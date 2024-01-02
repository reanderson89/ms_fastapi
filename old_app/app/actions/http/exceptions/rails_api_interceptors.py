from ..exceptions.rails_api_exceptions import Exceptions


def handle_response(execute):
    def interceptor(*args, **kwargs):
        response = execute()
        if response.status_code == 401:
            return Exceptions.rails_api401(response.reason)
        if response.status_code is not 200:
            return Exceptions.rails_api500(response.reason)

        return response.json()

    return interceptor
