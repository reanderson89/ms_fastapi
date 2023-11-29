import json
import os
from uuid import uuid4

import greenstalk

from app.configs.logging_format import init_logger
from app.utilities.decorators import handle_reconnect

logger = init_logger()

QUEUE_HOST = os.environ.get("JOB_QUEUE_HOST", "localhost")
QUEUE_PORT = int(os.environ.get("JOB_QUEUE_PORT", 11300))
QUEUE_TUBE = "milestone_response_tube"


class TempWorker:

    def __init__(self):
        self.conn = self.connect_to_greenstalk()

    def connect_to_greenstalk(self):
        return greenstalk.Client((QUEUE_HOST, QUEUE_PORT), use = "yass_tube", watch=QUEUE_TUBE)

    def reconnect(self):
        logger.milestone("Temp: Reconnecting to queue...")
        self.conn.close()
        self.conn = self.connect_to_greenstalk()

    @handle_reconnect
    async def temp_worker(self, job, tube, response_tube):
        job_id = uuid4().hex
        job["job_id"] = job_id
        self.conn.use(tube)
        self.conn.put(json.dumps(job))

        self.conn.watch(response_tube)

        while True:
            job_response = self.conn.reserve(timeout=5)
            if not job_response:
                return None
            job_data = json.loads(job_response.body)
            if job_data["job_id"] == job_id:
                self.conn.delete(job_response)
                return job_data
            else:
                self.conn.delete(job_response)
                # self.conn.release(job_response, delay=5)

    async def create_user_job(self, user_data: dict):
        job = {
            "eventType": "CREATE_USER",
            "source": "MILESTONES",
            "version": 0,
            "job_id": None,
            "respond_to": QUEUE_TUBE,
            "body": {"user": user_data}
        }
        response: dict = await self.temp_worker(job, "yass_tube", QUEUE_TUBE)
        return response.get("body")

    async def get_user_job(self, user_uuid: str):
        job = {
            "eventType": "GET_USER",
            "source": "MILESTONES",
            "version": 0,
            "job_id": None,
            "respond_to": QUEUE_TUBE,
            "body": {
                "user_uuid": user_uuid
            }
        }
        response = await self.temp_worker(job, "yass_tube", QUEUE_TUBE)
        return response["body"]

    async def alt_get_user_job(
        self,
        service_user_id: str
    ):
        job = {
            "eventType": "ALT_GET_USER",
            "source": "MILESTONES",
            "version": 0,
            "job_id": None,
            "respond_to": QUEUE_TUBE,
            "body": {
                "service_user_id": service_user_id
            }
        }
        response = await self.temp_worker(job, "yass_tube", QUEUE_TUBE)
        return response["body"]
