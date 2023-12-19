from ..exceptions.rails_api_exceptions import Exceptions
from functools import wraps


def catch_rails_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if response.status_code == 401:
            return Exceptions.rails_api401(response.reason)
        if response.status_code is not 200:
            return Exceptions.rails_api500(response.reason)
