from functools import wraps


def rails_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return {
            "Cookie": ""
        }
