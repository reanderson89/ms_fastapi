import os
import requests
from .authentication.rails_api_interceptors import rails_auth
from app.models.rails import RequestHeaders

RAILS_API = os.environ.get("RAILS_API")


class HttpRequests:
    @staticmethod
    def get_url(path: str):
        return f"{RAILS_API}{path}"

    @rails_auth
    # @handle_response
    @classmethod
    async def get(cls, path: str, headers: RequestHeaders = None):
        return requests.get(cls.get_url(path), headers=headers)

    # @rails_auth
    # @handle_response
    @classmethod
    async def post(cls, path: str, body: dict, headers: RequestHeaders = None):
        return requests.post(cls.get_url(path), headers=headers, json=body)

    # @rails_auth
    # @handle_response
    @classmethod
    async def put(cls, path: str, headers: RequestHeaders = None):
        response = requests.put(cls.get_url(path), headers=headers, json={})
        return response.json()

    @rails_auth
    # @handle_response
    @classmethod
    async def delete(cls, path: str, headers: RequestHeaders = None):
        return requests.delete(cls.get_url(path), headers=headers)
