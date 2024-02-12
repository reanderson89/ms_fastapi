import json
import sys

import greenstalk
from faker import Faker

from app.worker.logging_format import init_logger
from app.worker.utils import WorkerUtils

logger = init_logger()
faker = Faker()

QUEUE_HOST = "localhost"
QUEUE_PORT = 11300
QUEUE_TUBE = "milestones_tube"


def handle_reconnect(func):
    def wrapper(self, *args, **kwargs):
        retries = 3
        for _ in range(retries):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                print(f"Error in {func.__name__}: {e}")
                self.reconnect()
        print(f"Failed to execute {func.__name__} after {retries} retries.")
    return wrapper


class CronJobs:
    def __init__(self):
        self.conn = self.connect_to_greenstalk()

    def connect_to_greenstalk(self):
        return greenstalk.Client((QUEUE_HOST, QUEUE_PORT), use=QUEUE_TUBE)

    def reconnect(self):
        print("Reconnecting to queue...")
        self.conn.close()
        self.conn = self.connect_to_greenstalk()

    @handle_reconnect
    def put_job(self, job, tube=None):
        if tube:
            self.conn.use(tube)
        else:
            self.conn.use(QUEUE_TUBE)
        self.conn.put(json.dumps(job))

    def reward_cron_job(self):
        return WorkerUtils.build_job_payload(
            event_type="CRON_JOB",
            source="CRON",
            response_body={
                "auth": 1234,
                "company_id": faker.uuid4()
            }
        )

    def main(self):
        try:
            job = self.reward_cron_job()
            self.put_job(job)
            print("Cron job sent to queue.")
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)


if __name__ == "__main__":
    cron_jobs = CronJobs()
    cron_jobs.main()
