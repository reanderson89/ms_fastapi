import boto3
from threading import Lock
from mypy_boto3_sqs import SQSClient


class SQSClientSingleton:
    _instance = None
    _lock = Lock()

    @classmethod
    def get_instance(cls, region_name, endpoint_url):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance: SQSClient = boto3.client("sqs", region_name=region_name, endpoint_url=endpoint_url)
        return cls._instance

    @classmethod
    def reconnect(cls, region_name, endpoint_url):
        with cls._lock:
            cls._instance: SQSClient = boto3.client("sqs", region_name=region_name, endpoint_url=endpoint_url)
        return cls._instance
