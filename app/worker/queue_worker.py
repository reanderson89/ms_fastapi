import json
import os
import time

import greenstalk

from app.actions.clients.user import ClientUserActions
from app.configs.logging_format import init_logger
from app.utilities.decorators import handle_reconnect
from burp.models.user import UserModel
from app.models.clients import ClientUserExpand

logger = init_logger()

QUEUE_HOST = os.environ.get("JOB_QUEUE_HOST", "localhost")
QUEUE_PORT = int(os.environ.get("JOB_QUEUE_PORT", 11300))
QUEUE_TUBE = os.environ.get("JOB_QUEUE_TUBE", "milestones_tube")


class QueueWorker:

    def __init__(self):
        self.conn = self.connect_to_greenstalk()

    def connect_to_greenstalk(self):
        return greenstalk.Client((QUEUE_HOST, QUEUE_PORT), watch=QUEUE_TUBE)

    def reconnect(self):
        logger.milestone("Reconnecting to queue...")
        self.conn.close()
        self.conn = self.connect_to_greenstalk()

    def put_in_dlq(self, job, reason):
        job_data = json.loads(job.body)
        job_data["issue"] = reason
        self.conn.use("milestones_dlq")
        self.conn.put(json.dumps(job_data))
        self.conn.use(QUEUE_TUBE)
        self.conn.delete(job)

    async def send_response(self, job_data: dict, response_body: dict):
        job = self.response_job(response_body, job_data.get("job_id"))
        self.conn.use(job_data["respond_to"])
        self.conn.put(json.dumps(job))
        self.conn.use(QUEUE_TUBE)
        return True
    
    def response_job(self, response_body: dict, job_id: str):
        return {
            "eventType": "USER_RESPONSE",
            "source": "YASS",
            "version": 0,
            "job_id": job_id,
            "body": response_body
        }

    @handle_reconnect
    async def worker(self):
        logger.milestone("Starting Survey Consumer...")
        while True:
            job = self.conn.reserve()
            job_data = json.loads(job.body)

            start_time = time.time()
            try:
                should_delete, reason = await self.consume_job(job_data)

                if should_delete:
                    self.conn.delete(job)
                else:
                    self.put_in_dlq(job, reason)

            except Exception as e:
                logger.milestone(f"Worker error processing job: {str(e)}")
                self.put_in_dlq(job, str(e))

            end_time = time.time()
            duration = end_time - start_time
            logger.milestone(f"{job_data['eventType']} job processed in {format(duration, '.5f')} seconds!")

    async def consume_job(self, job_data: dict):
        event_type = job_data.get("eventType")

        try:
            match event_type:
                case "MOCK_REWARD_SCHEDULED":
                    # time.sleep(.5)
                    logger.milestone(f"Test: Reward scheduled for {job_data['body']['recipient']['name']}")
                    return True, "Processed"
                case "MOCK_GET_SURVEY_RESPONSE":
                    # time.sleep(.5)
                    logger.milestone(f"Test: Survey response received for Survey {job_data['body']['surveyId']}")
                    return True, "Processed"
                case "CREATE_CLIENT_USER":
                    new_user = await ClientUserActions.handle_client_user_job(job_data)
                    if type(new_user) is UserModel:
                        logger.milestone(f"User created for {new_user.first_name} {new_user.last_name}")
                    elif type(new_user) is ClientUserExpand:
                        logger.milestone(f"Client User created for {new_user.user.first_name} {new_user.user.last_name}")
                    return True, "Processed"
                case "MIGRATE_USER":
                    response = await self.migrate_user(job_data)
                    return response, "Processed"
                case _:
                    return False, "No matching event type found"
        except Exception as e:
            logger.milestone(f"Consumer error processing job: {str(e)}")
            return False, "Error processing job"
        

    async def migrate_user(self, job_data: dict):
        body = job_data.get("body")
        migrated_user = await ClientUserActions.migrate_user(body["current_user_uuid"], body["old_user_uuid"])
        if migrated_user:
            logger.milestone(f"Milestones migration of user info successful.")
            response = await self.send_response(job_data, {"migration_completed":True})
        else:
            logger.milestone(f"Milestone migration of user info was not successful.")
            response = await self.send_response(job_data, {"migration_completed":True})
        return response