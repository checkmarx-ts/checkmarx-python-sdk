import requests
from .config import config
from . import authHeaders
from ..compat import (OK, UNAUTHORIZED, CREATED)


def retry_when_unauthorized(func):
    """

    Args:
        func (function)

    Returns:
        function
    """
    def retry(*args, **kwargs):
        max_try = 3

        response = func(*args, **kwargs)

        while max_try > 0:
            if response.status_code != UNAUTHORIZED:
                break
            authHeaders.update_auth_headers()
            response = func(*args, **kwargs)
            max_try -= 1

        return response
    return retry


def http_get(relative_url):
    url = config.get("reporting_client_url") + relative_url
    response = requests.get(
        url=url,
        headers=authHeaders.auth_headers,
        verify=False
    )

    if response.status_code not in [OK, UNAUTHORIZED]:
        raise ValueError("HttpStatusCode: {code}".format(code=response.status_code),
                         "ErrorMessage: {msg}".format(msg=response.text))
    return response


def http_post(relative_url, data):
    url = config.get("reporting_client_url") + relative_url
    response = requests.post(
        url=url,
        data=data,
        headers=authHeaders.auth_headers,
        verify=False
    )

    if response.status_code not in [OK, CREATED, UNAUTHORIZED]:
        raise ValueError("HttpStatusCode: {code}".format(code=response.status_code),
                         "ErrorMessage: {msg}".format(msg=response.text))

    return response


@retry_when_unauthorized
def get_request(relative_url):
    return http_get(relative_url)


@retry_when_unauthorized
def post_request(relative_url, data):
    return http_post(relative_url, data)
