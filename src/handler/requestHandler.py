import requests
from constant import base_url

# def request_error():

class RequestHelper:
    def __init__(self) -> None:
        pass

    def get(self, endpoint, params=None, data=None, json=None):
        try:
            url = f"{base_url}/{endpoint}"
            response = requests.get(url, params=params, data=data, json=json)

            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    def post(self, endpoint, data=None, json=None, files=None):
        try:
            url = f"{base_url}/{endpoint}"
            response = requests.post(url, data=data, json=json, files=files)

            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    def patch(self, endpoint, data=None, json=None):
        try:
            url = f"{base_url}/{endpoint}"
            response = requests.patch(url, data=data, json=json)

            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    @staticmethod
    def _handle_response(response):
        if response.status_code == 200:
            return response.json()
        else:
            return RequestHelper._handle_error(response.status_code)

    @staticmethod
    def _handle_error(error):
        if isinstance(error, int):
            status_code = error
            error_msg = f"Request failed with status code: {status_code}"
        else:
            status_code = None
            error_msg = f"An error occurred: {str(error)}"

        print(error_msg)
        return None