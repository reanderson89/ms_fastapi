import json
import os
import statistics
import sys
import time

import greenstalk
import numpy as np
from faker import Faker

from app.configs.logging_format import init_logger
logger = init_logger()


faker = Faker()

QUEUE_HOST = os.environ.get("JOB_QUEUE_HOST", "localhost")
QUEUE_PORT = int(os.environ.get("JOB_QUEUE_PORT", 11300))
QUEUE_TUBE = os.environ.get("JOB_QUEUE_TUBE", "milestone_tube")
ya_tube = "yass_tube"
ms_tube = "milestone_tube"


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


class JobProducer:
    def __init__(self):
        self.conn = self.connect_to_greenstalk()

    def connect_to_greenstalk(self):
        return greenstalk.Client((QUEUE_HOST, QUEUE_PORT), use=QUEUE_TUBE)

    def reconnect(self):
        print("Reconnecting to queue...")
        self.conn.close()
        self.conn = self.connect_to_greenstalk()

    def fake_bday(self):
        return int(faker.date_time_between(start_date="-50y", end_date="-18y").timestamp())

    def reward_job(self):
        return {
            "eventType": "MOCK_REWARD_SCHEDULED",
            "source": "GSD",
            "version": 0,
            "body": {
                "surveyId": "aebQTOSw",
                "experience": {
                    "concierge": "Jennifer",
                    "name": "Skydiving"
                },
                "recipient": {
                    "name": "Jane Doe",
                    "email": "jane@doe.com"
                }
            }
        }

    def survey_job(self):
        return {
            "eventType": "MOCK_GET_SURVEY_RESPONSE",
            "body": {
                "surveyId": "aebQTOSw"
            }
        }

    def wrong_job(self):
        return {
            "eventType": "WRONG_EVENT_TYPE",
            "body": {
                "dogs_name": "Spot"
            }
        }

    def user_job(self):
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@testmail.com"

        return {
            "eventType": "CREATE_USER",
            "source": "GSD",
            "version": 0,
            "body": {
                "user": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email
                }
            }
        }

    def client_user_job(self):
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@testmail.com"

        return {
            "eventType": "CREATE_CLIENT_USER",
            "source": "GSD",
            "version": 0,
            "body": {
                "client_uuid": "ca723b34b08e4e319c8d2e6770815679c69aaf4a8e574f518b1e34",
                "user": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "work_email": email
                }
            }
        }

    def produce_jobs(self):
        jobs = [
            self.reward_job(),
            self.survey_job()
        ]
        for _ in range(10):
            for job in jobs:
                self.put_job(job)

    @handle_reconnect
    def put_job(self, job, tube=None):
        if tube:
            self.conn.use(tube)
        else:
            self.conn.use(QUEUE_TUBE)
        self.conn.put(json.dumps(job))

    def not_looped(self, batches):
        logger.gsd_producer(f"Producing {batches*20} jobs...")
        for i in range(1, batches + 1):
            self.produce_jobs()
            if i % 10 == 0:
                print(f"Jobs produced: {i*20}")
        print("-" * 20)

    @handle_reconnect
    def loop_jobs(self):
        logger.gsd_producer("Starting Looped Job Producer...")
        last_job_count = None
        times = []
        batch_averages = []
        beginning_start_time = time.time()
        start_time = time.time()

        try:
            while True:
                job_total = int(self.conn.stats_tube("yass_tube")["current-jobs-ready"])

                if job_total != last_job_count or job_total == 0:
                    if job_total <= 20:
                        end_time = time.time()
                        times.append(end_time - start_time)
                        avg_time = sum(times) / len(times)
                        batch_averages.append(avg_time)
                        logger.gsd_producer(f"Average time for this batch of jobs: {avg_time:.5f} sec")
                        start_time = time.time()  # reset start_time
                        times = []  # reset times
                        self.produce_jobs()
                    else:
                        pass

                    last_job_count = job_total
        except KeyboardInterrupt:
            if batch_averages:
                batch_averages.remove(min(batch_averages))
            if batch_averages:
                total_avg = sum(batch_averages) / len(batch_averages)
                rolling_avg = sum(batch_averages[-5:]) / min(5, len(batch_averages))
                total_time = time.time() - beginning_start_time
                min_time = min(batch_averages)
                max_time = max(batch_averages)
                if len(batch_averages) >= 2:
                    std_dev = statistics.stdev(batch_averages)
                else:
                    std_dev = 0
                percentile_95 = np.percentile(batch_averages, 95)
                print("\nResults:")
                print(f"Total average time: {total_avg:.5f} sec")
                print(f"Rolling average time for the last 5 batches: {rolling_avg:.5f} sec")
                print(f"Min time: {min_time:.5f} sec")
                print(f"Max time: {max_time:.5f} sec")
                print(f"Standard deviation: {std_dev:.5f} sec")
                print(f"95th percentile time: {percentile_95:.5f} sec")
                print(f"Total batches: {len(batch_averages)}")
                print(f"Total jobs created: {len(batch_averages) * 20}")
                print(f"Total elapsed time: {total_time:.5f} sec")

                print("-" * 20)

    @handle_reconnect
    def add_job_interactively(self, job_type=None):
        try:
            while True:
                if not job_type:
                    job_type = input(
                        "Select the type of job to add to the queue:\n"
                        "  1: CREATE_USER\n"
                        "  2: CREATE_CLIENT_USER\n"
                        "  3: MOCK_REWARD_SCHEDULED\n"
                        "  4: MOCK_GET_SURVEY_RESPONSE\n"
                        "  5: Misnamed Job -> Dead Letter Queue\n"
                        "  6: Start Looped Job Producer\n"
                        "  7: Add 1k jobs\n"
                        "  8: Exit\n"
                        "----------------\n"
                        "Your choice: "
                    )

                match job_type:
                    case "1":
                        job = self.user_job()
                        status = self.conn.stats_tube(ms_tube)["current-jobs-ready"]
                        self.put_job(job, ya_tube)
                        print(f"{QUEUE_TUBE} Jobs: {status}\n")
                    case "2":
                        job = self.client_user_job()
                        status = self.conn.stats_tube(QUEUE_TUBE)["current-jobs-ready"]
                        self.put_job(job, ms_tube)
                        print(f"{QUEUE_TUBE} Jobs: {status}\n")
                    case "3":
                        job = self.reward_job()
                        status = self.conn.stats_tube(QUEUE_TUBE)["current-jobs-ready"]
                        self.put_job(job)
                        print(f"{QUEUE_TUBE} Jobs: {status}\n")
                    case "4":
                        job = self.survey_job()
                        status = self.conn.stats_tube(QUEUE_TUBE)["current-jobs-ready"]
                        self.put_job(job)
                        print(f"{QUEUE_TUBE} Jobs: {status}\n")
                    case "5":
                        job = self.wrong_job()
                        self.put_job(job)
                        time.sleep(.1)
                        status = self.conn.stats_tube(QUEUE_TUBE)["current-jobs-ready"]
                        dlq_status = self.conn.stats_tube("milestone_dlq")["current-jobs-ready"]
                        print(f"{QUEUE_TUBE} Jobs: {status}\nmilestone_dlq Jobs: {dlq_status}\n")
                    case"6":
                        self.loop_jobs()
                    case "7":
                        self.not_looped(50)
                    case "8":
                        break
                    case _:
                        print("Invalid selection.")
                job_type = None
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting...")
            sys.exit(0)


if __name__ == "__main__":
    producer = JobProducer()
    producer.add_job_interactively()
