import json
import os
import time

import greenstalk
from fastapi import HTTPException

from app.actions.clients.user import ClientUserActions
from app.models.clients import ClientUserExpand
from app.utilities.decorators import handle_reconnect
from app.worker.logging_format import init_logger
from app.worker.utils import build_job_payload
from burp.models.user import UserModel

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
        logger.milestone("[Worker] Reconnecting to queue...")
        self.conn.close()
        self.conn = self.connect_to_greenstalk()

    @handle_reconnect
    def put_job(self, job_data: dict, tube: str = None):
        tube = tube or QUEUE_TUBE
        self.conn.use(tube)
        self.conn.put(json.dumps(job_data))

    def put_in_dlq(self, job, reason):
        job_data = json.loads(job.body)
        job_data["issue"] = reason
        self.put_job(job_data, "milestones_dlq")
        self.conn.delete(job)

    async def error_response(self, job, job_data: dict, error_message: str):
        if job_data.get("response_tube"):
            await self.send_response(job_data, {error_message}, status="error")
        self.put_in_dlq(job, error_message)

    async def send_response(self, job_data: dict, response_body: dict, status: str = None):
        job = self.response_job(job_data, response_body, status)
        self.put_job(job, tube=job_data["response_tube"])
        return True

    def response_job(self, job_data: dict, response_body: dict, status: str = None):
        response_payload = build_job_payload(
            event_type=f"{job_data['eventType']}_RESPONSE",
            source="MILESTONES",
            response_body=response_body,
            job_id=job_data["job_id"],
            response_tube=job_data["response_tube"],
            response_status=status or "success"
        )
        return response_payload

    @handle_reconnect
    async def worker(self):
        logger.milestone("Worker is watching...")
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

            except HTTPException as e:
                event_type = job_data.get("eventType")
                job_error = f"HTTP error processing {event_type} job: {e.detail}"
                logger.milestone(f"[Worker] HTTP error processing {event_type} job: {e.detail}")
                await self.error_response(job, job_data, {"error": f"{job_error}"})
            except Exception as e:
                event_type = job_data.get("eventType")
                job_error = f"Error processing job . {e.__class__.__name__}: {e}"
                logger.milestone(f"[Worker] Job error: {str(e)}")
                await self.error_response(job, job_data, {"error": f"{job_error}"})

            end_time = time.time()
            duration = end_time - start_time
            logger.milestone(f"{job_data['eventType']} job processed in {format(duration, '.5f')} seconds!")

    async def consume_job(self, job_data: dict):
        event_type = job_data.get("eventType")
        logger.milestone(f"Starting {event_type} job...")

        # try:
        match event_type:
            case "MOCK_REWARD_SCHEDULED":
                logger.milestone(f"Reward scheduled for {job_data['body']['recipient']['name']}")
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

    async def migrate_user(self, job_data: dict):
        body = job_data.get("body")
        migrated_user = await ClientUserActions.migrate_user(body["current_user_uuid"], body["old_user_uuid"])
        if migrated_user:
            logger.milestone("Milestones migration of user info successful.")
            response = await self.send_response(job_data, {"migration_completed":True})
        else:
            logger.milestone("Milestone migration of user info was not successful.")
            response = await self.send_response(job_data, {"migration_completed":True})
        return response
