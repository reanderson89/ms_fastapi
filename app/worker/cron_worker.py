import asyncio
import os
import time
import json
from concurrent.futures import ThreadPoolExecutor

from botocore.exceptions import EndpointConnectionError
from fastapi import HTTPException
from mypy_boto3_sqs import SQSClient

from app.actions.cron.cron_actions import CronActions
from app.actions.rewards.staged_reward_actions import StagedRewardActions
from app.models.reward.reward_models import RailsCreateRewardResponse
from app.utilities.decorators import handle_reconnect
from app.worker.logging_format import init_logger
from app.worker.sqs_client_config import SQSClientSingleton
from app.worker.utils import WorkerUtils

logger = init_logger("Cron Worker")

RETRY_DELAY = 1  # Delay between retries in seconds
MAX_RETRIES = 3  # Maximum number of retries

REWARDS_QUEUE = os.environ.get("REWARDS_QUEUE_URL", "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/localstack-rewards")


class CronWorker:

    def __init__(self):
        self.default_queue = REWARDS_QUEUE
        self.queue_name = WorkerUtils.get_queue_name(self.default_queue)
        self.conn: SQSClient = SQSClientSingleton.get_instance(self.default_queue)
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=1)

    def reconnect(self):
        logger.milestone("Reconnecting to queue...")
        self.conn = SQSClientSingleton.reconnect(self.default_queue)

    @handle_reconnect
    def send_message(self, message: dict, queue_url: str):
        response = self.conn.send_message(
            QueueUrl=queue_url,
            DelaySeconds=1,
            MessageBody=json.dumps(message),
        )
        logger.milestone(response)

    def update_message_visibility(self, receipt_handle, queue):
        logger.milestone("Unable to process job. Putting job back in queue.")
        self.conn.change_message_visibility(
            QueueUrl=queue,
            ReceiptHandle=receipt_handle,
            VisibilityTimeout=0
        )

    async def send_response(self, job_data: dict, response_body: dict, status: str = None):
        job = self.response_job(job_data, response_body, status)
        self.send_message(job, queue_url=job_data["response_tube"])
        return True

    def response_job(self, job_data: dict, response_body: dict, status: str = None):
        response_payload = WorkerUtils.build_job_payload(
            event_type=f"{job_data['eventType']}_RESPONSE",
            source="MILESTONES",
            response_body=response_body,
            job_id=job_data["job_id"],
            response_tube=job_data["response_tube"],
            response_status=status or "success"
        )
        return response_payload

    async def worker(self):
        logger.milestone(f"Watching \033[92m{self.queue_name}\033[0m queue...")
        while True:
            for _ in range(MAX_RETRIES):
                try:
                    # runs in a separate thread to avoid blocking the event loop
                    messages_received = await self.loop.run_in_executor(
                        self.executor,
                        lambda: self.conn.receive_message(
                            QueueUrl=self.default_queue,
                            AttributeNames=["SentTimestamp"],
                            MaxNumberOfMessages=1,  # TODO: only will get a single message right now
                            MessageAttributeNames=["string",],
                            VisibilityTimeout=30,
                            WaitTimeSeconds=20
                        )
                    )
                    break
                except self.conn.exceptions.QueueDoesNotExist:
                    logger.milestone("Queue does not exist.")
                    await asyncio.sleep(RETRY_DELAY)
                    logger.milestone("Retrying to receive messages...")
                    continue
                except EndpointConnectionError:
                    logger.milestone("Endpoint connection error.")
                    self.reconnect()
                    continue
                except asyncio.CancelledError:
                    logger.milestone("Worker cancelled.")
                    return
                except Exception as e:
                    error_name = e.__class__.__name__
                    logger.milestone(f"Error receiving messages: {error_name}-{e}")
                    raise e

            else:
                # If we've exhausted all retries and still failed, reconnect
                self.reconnect()
                continue

            if "Messages" not in messages_received.keys():
                continue

            logger.milestone("Message recieved")
            start_time = time.time()
            # logger.milestone(messages_received)
            # TODO: picking off the top message (only getting one anyway)
            for msg_data in messages_received["Messages"]:
                msg_body_dict: dict = json.loads(msg_data.get("Body") or "")
                receipt_handle = msg_data.get("ReceiptHandle")
                try:
                    await self.process_job(msg_body_dict, receipt_handle)
                except Exception as e:
                    error_name = e.__class__.__name__
                    if error_name == "ReceiptHandleIsInvalid":
                        continue

            end_time = time.time()
            duration = end_time - start_time
            logger.milestone(f"{msg_body_dict['eventType']} Message processed in {format(duration, '.5f')} seconds!")

    async def process_job(self, msg_body_dict, receipt_handle):
        try:
            should_delete = await self.consume_job(msg_body_dict)

            if should_delete:
                self.conn.delete_message(
                    QueueUrl=self.default_queue,
                    ReceiptHandle=receipt_handle
                )
            else:
                self.update_message_visibility(receipt_handle, self.default_queue)

        except HTTPException as e:
            event_type = msg_body_dict.get("eventType")
            msg_error = f"HTTP error processing {event_type} job: {e.detail}"
            logger.milestone(f"[Worker] {msg_error}")
            self.update_message_visibility(receipt_handle, self.default_queue)

        except Exception as e:
            error_name = e.__class__.__name__
            if error_name == "ReceiptHandleIsInvalid":
                logger.milestone("Receipt handle is invalid.")
                raise e
            event_type = msg_body_dict.get("eventType")
            msg_error = f"Error processing job . {e.__class__.__name__}: {e}"
            logger.milestone(f"[Worker] {msg_error}")
            self.update_message_visibility(receipt_handle, self.default_queue)

    async def consume_job(self, msg_data: dict):
        response = False
        event_type = msg_data.get("eventType")
        logger.milestone(f"Starting {event_type} job...")

        match event_type:
            case "TEST_MILESTONES_REWARDS_QUEUE":
                logger.milestone(f"Test message received in Rewards Queue: {msg_data['body']}")
                response = True
            case "HANDLE_POST_RAILS_REWARD_CREATE":
                response = await self.handle_post_rails_reward_create(msg_data['body'])
            case _:
                # No matching event type found
                logger.milestone(f"No matching event type found for {event_type}.")
                response = False
        return response
    
    async def handle_post_rails_reward_create(self, body):
        rails_response = RailsCreateRewardResponse(**body)
        staged_reward = await StagedRewardActions.get_staged_reward(rails_response.staged_reward_uuid)
        try:
            return await CronActions.handle_staged_reward_state_update(staged_reward, rails_response)
        except:
            return False