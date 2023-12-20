import os
import requests
import json
from .exceptions.rails_api_interceptors import catch_rails_exceptions
# from .authentication.rails_api_interceptors import rails_auth

# Hard coded for now. Would like to use an interceptor for the auth.
HEADERS = {
    "Cookie": ""
}

RAILS_API = os.environ.get("RAILS_API")


class HttpRequests:
    @staticmethod
    def get_url(path: str):
        return f"{RAILS_API}{path}"

    # @rails_auth
    # @catch_rails_exceptions
    @classmethod
    async def get(cls, path: str, query_params: dict):
        response = requests.get(cls.get_url(path), headers=HEADERS)
        return response.json()

    # @rails_auth
    @catch_rails_exceptions
    @classmethod
    async def post(cls, path: str, body: dict):
        response = requests.post(cls.get_url(path), headers=HEADERS, json=json.dumps(body))
        return response.json()

    # @rails_auth
    # @catch_rails_exceptions
    @classmethod
    async def put(cls, path: str):
        response = requests.put(cls.get_url(path), headers=HEADERS)
        return response.json()

    # @rails_auth
    # @catch_rails_exceptions
    @classmethod
    async def delete(cls, path: str):
        response = requests.delete(cls.get_url(path), headers=HEADERS)
        return response.json()
