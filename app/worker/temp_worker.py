import ast
import os
from time import time
from uuid import uuid4

from fastapi import HTTPException
from mypy_boto3_sqs import SQSClient

from app.utilities.decorators import handle_reconnect
from app.worker.logging_format import init_logger
from app.worker.sqs_client_config import SQSClientSingleton
from app.worker.utils import WorkerUtils
from burp.models.reward import ProgramRuleModelDB

logger = init_logger("Temp Worker")

SEGMENT_QUEUE = os.environ.get("SEGMENT_QUERY_QUEUE_URL", "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/localstack-segment-query")
RESPONSE_QUEUE = os.environ.get("SEGMENT_RESPONSE_QUEUE_URL", "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/localstack-segment-response")


class TempWorker:

    def __init__(self):
        self.conn: SQSClient = SQSClientSingleton.get_instance(RESPONSE_QUEUE)

    def reconnect(self):
        logger.milestone("Reconnecting to queue...")
        self.conn = SQSClientSingleton.reconnect(RESPONSE_QUEUE)

    @handle_reconnect
    def send_message(self, message: dict, queue_url: str):
        response = self.conn.send_message(
            QueueUrl=queue_url,
            DelaySeconds=0,
            MessageBody=str(message),
        )
        logger.milestone(response)

    def update_message_visibility(self, receipt_handle, queue):
        self.conn.change_message_visibility(
            QueueUrl=queue,
            ReceiptHandle=receipt_handle,
            VisibilityTimeout=0
        )

    @handle_reconnect
    async def response_worker(self, job: dict, queue, response_queue):
        msg_data = {}
        try:
            job_id = uuid4().hex
            job["job_id"] = job_id
            self.send_message(job, queue)

            start_time = time()
            while True:
                if time() - start_time > 5:
                    raise Exception("Temp worker timed out waiting for response.")

                msg_response = self.conn.receive_message(
                    QueueUrl=response_queue,
                    AttributeNames=["SentTimestamp"],
                    # TODO: only will get a single message right now
                    MaxNumberOfMessages=1,
                    MessageAttributeNames=["string",],
                    VisibilityTimeout=30,
                    WaitTimeSeconds=20
                )
                if not msg_response:
                    return None
                msg_data = msg_response["Messages"][0]
                msg_body_dict: dict = ast.literal_eval(msg_data.get("Body") or "")
                receipt_handle = msg_data.get("ReceiptHandle")
                if msg_body_dict["job_id"] == job_id:
                    self.conn.delete_message(
                        QueueUrl=RESPONSE_QUEUE,
                        ReceiptHandle=receipt_handle
                    )
                    return msg_body_dict
                else:
                    self.update_message_visibility(msg_response.receipt_handle, response_queue)
        except HTTPException as e:
            event_type = msg_data.get("eventType")
            logger.milestone(f"HTTP error processing {event_type} job: {e.detail}")
            self.update_message_visibility(msg_response.receipt_handle, response_queue)
        except Exception as e:
            event_type = msg_data.get("eventType")
            logger.milestone(f"{event_type} job error: {e.__class__.__name__}: {e}")
            self.update_message_visibility(msg_response.receipt_handle, response_queue)

    async def get_user_job(self, user_uuid: str):
        job = WorkerUtils.build_job_payload(
            "GET_USER",
            "MILESTONES",
            {"user_uuid": user_uuid},
            RESPONSE_QUEUE
        )
        response = await self.response_worker(job, SEGMENT_QUEUE, RESPONSE_QUEUE)
        user = response.get("body") if response else None
        if response["response_status"] == "error":
            raise Exception(f"Milestones ran into an issue. {user['error']}")
        return user

    async def alt_get_user_job(
        self,
        service_user_id: str
    ):
        job = WorkerUtils.build_job_payload(
            "ALT_GET_USER",
            "MILESTONES",
            {"service_user_id": service_user_id},
            RESPONSE_QUEUE
        )
        response = await self.response_worker(job, SEGMENT_QUEUE, RESPONSE_QUEUE)
        user = response.get("body") if response else None
        if response["response_status"] == "error":
            raise Exception(f"Milestones ran into an issue. {user['error']}")
        return user

    def get_users_for_reward_creation(
        self,
        rule: ProgramRuleModelDB
    ):
        job = WorkerUtils.build_job_payload(
            "GET_USERS_FOR_REWARD_CREATION",
            "MILESTONES",
            rule.to_dict(),
            RESPONSE_QUEUE
        )
        self.send_message(job, SEGMENT_QUEUE)
