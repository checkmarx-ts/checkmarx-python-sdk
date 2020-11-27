import requests

from . import authHeaders
from ..config import config
from ..compat import (OK, UNAUTHORIZED)


def retry_when_unauthorized(func):
    """

    Args:
        func (function)

    Returns:
        function
    """
    def retry(*args, **kwargs):
        max_try = config.get('max_try')

        response = func(*args, **kwargs)

        while max_try > 0:
            if response.status_code != UNAUTHORIZED:
                break
            authHeaders.update_auth_headers()
            response = func(*args, **kwargs)
            max_try -= 1

        if response.status_code != OK:
            raise ValueError("HttpStatusCode: {code}".format(code=response.status_code),
                             "ErrorMessage: {msg}".format(msg=response.text))

        return response
    return retry


def get_value_from_response(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs).json().get("value")
    return inner


def http_get(relative_url):
    url = config.get("base_url") + relative_url
    return requests.get(
        url=url,
        headers=authHeaders.auth_headers,
        auth=authHeaders.basic_auth,
        verify=config.get("verify")
    )


@get_value_from_response
@retry_when_unauthorized
def get_request(relative_url):
    return http_get(relative_url)


@retry_when_unauthorized
def get_request_with_raw_response(relative_url):
    return http_get(relative_url)
