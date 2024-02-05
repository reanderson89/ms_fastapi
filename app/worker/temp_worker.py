import json
import os
from time import time
from uuid import uuid4

import greenstalk
from fastapi import HTTPException

from app.worker.logging_format import init_logger
from app.utilities.decorators import handle_reconnect
from app.worker.utils import build_job_payload
from burp.models.reward import ProgramRuleModelDB

logger = init_logger()

QUEUE_HOST = os.environ.get("JOB_QUEUE_HOST", "localhost")
QUEUE_PORT = int(os.environ.get("JOB_QUEUE_PORT", 11300))
QUEUE_TUBE = "milestone_response_tube"


class TempWorker:

    def __init__(self):
        self.conn = self.connect_to_greenstalk()

    def connect_to_greenstalk(self):
        return greenstalk.Client((QUEUE_HOST, QUEUE_PORT), use="yass_tube", watch=QUEUE_TUBE)

    def reconnect(self):
        logger.milestone("[Temp Worker] Reconnecting to queue...")
        self.conn.close()
        self.conn = self.connect_to_greenstalk()

    @handle_reconnect
    def put_job(self, job_data: dict, tube: str = None):
        tube = tube or QUEUE_TUBE
        self.conn.use(tube)
        self.conn.put(json.dumps(job_data))

    @handle_reconnect
    async def temp_worker(self, job, tube, response_tube):
        try:
            job_id = uuid4().hex
            job["job_id"] = job_id
            self.put_job(job, tube)

            self.conn.watch(response_tube)

            start_time = time()
            while True:
                if time() - start_time > 5:
                    raise Exception("Temp worker timed out waiting for response.")

                job_response = self.conn.reserve(timeout=2)
                if not job_response:
                    return None
                job_data = json.loads(job_response.body)
                if job_data["job_id"] == job_id:
                    self.conn.delete(job_response)
                    return job_data
                else:
                    self.conn.release(job_response, delay=5)
                    # self.conn.delete(job_response)
        except greenstalk.TimedOutError:
            event_type = job.get("eventType")
            logger.milestone(f"[Temp Worker] Timeout error processing {event_type} job.")
            raise Exception(f"Temp worker timed out waiting for {event_type} response.")
        except HTTPException as e:
            event_type = job_data.get("eventType")
            logger.milestone(f"[Temp Worker] HTTP error processing {event_type} job: {e.detail}")
        except Exception as e:
            event_type = job_data.get("eventType")
            logger.milestone(f"[Temp Worker] {event_type} job error: {e.__class__.__name__}: {e}")

    async def create_user_job(self, user_data: dict):
        job = build_job_payload(
            "CREATE_USER",
            "MILESTONES",
            {"user": user_data},
            QUEUE_TUBE
        )
        response: dict = await self.temp_worker(job, "yass_tube", QUEUE_TUBE)
        user = response.get("body") if response else None
        if response["response_status"] == "error":
            raise Exception(f"Yass ran into an issue. {user['error']}")
        return user

    async def get_user_job(self, user_uuid: str):
        job = build_job_payload(
            "GET_USER",
            "MILESTONES",
            {"user_uuid": user_uuid},
            QUEUE_TUBE
        )
        response = await self.temp_worker(job, "yass_tube", QUEUE_TUBE)
        user = response.get("body") if response else None
        if response["response_status"] == "error":
            raise Exception(f"Yass ran into an issue. {user['error']}")
        return user

    async def alt_get_user_job(
        self,
        service_user_id: str
    ):
        job = build_job_payload(
            "ALT_GET_USER",
            "MILESTONES",
            {"service_user_id": service_user_id},
            QUEUE_TUBE
        )
        response = await self.temp_worker(job, "yass_tube", QUEUE_TUBE)
        user = response.get("body") if response else None
        if response["response_status"] == "error":
            raise Exception(f"Yass ran into an issue. {user['error']}")
        return user

    def get_users_for_reward_creation(
        self,
        rule: ProgramRuleModelDB
    ):
        job = build_job_payload(
            "GET_USERS_FOR_REWARD_CREATION",
            "MILESTONES",
            rule.to_dict()
        )
        self.put_job(job, "yass_tube")



