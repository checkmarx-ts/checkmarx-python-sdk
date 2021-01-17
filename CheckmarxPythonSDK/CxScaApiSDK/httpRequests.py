import requests
from ..config import sca_config
from . import authHeaders
from ..compat import (OK, UNAUTHORIZED, NO_CONTENT, CREATED)


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


def get_value_from_response(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs).json()
    return inner


def http_get(relative_url):
    url = sca_config.get("server") + relative_url
    response = requests.get(
        url=url,
        headers=authHeaders.auth_headers,
        verify=False
    )

    if response.status_code != OK:
        raise ValueError("HttpStatusCode: {code}".format(code=response.status_code),
                         "ErrorMessage: {msg}".format(msg=response.text))
    return response


def http_post(relative_url, data):
    url = sca_config.get("server") + relative_url
    response = requests.post(
        url=url,
        data=data,
        headers=authHeaders.auth_headers,
        verify=False
    )

    if response.status_code not in [OK, CREATED]:
        raise ValueError("HttpStatusCode: {code}".format(code=response.status_code),
                         "ErrorMessage: {msg}".format(msg=response.text))

    return response


def http_put(relative_url, data, headers=None):

    if not headers:
        headers = authHeaders.auth_headers

    url = sca_config.get("server") + relative_url
    response = requests.put(
        url=url,
        data=data,
        headers=headers,
        verify=False
    )
    if response.status_code != NO_CONTENT:
        raise ValueError("HttpStatusCode: {code}".format(code=response.status_code),
                         "ErrorMessage: {msg}".format(msg=response.text))
    return response


def http_delete(relative_url):
    url = sca_config.get("server") + relative_url
    response = requests.delete(
        url=url,
        headers=authHeaders.auth_headers,
        verify=False
    )

    if response.status_code != NO_CONTENT:
        raise ValueError("HttpStatusCode: {code}".format(code=response.status_code),
                         "ErrorMessage: {msg}".format(msg=response.text))

    return response


@get_value_from_response
@retry_when_unauthorized
def get_request(relative_url):
    return http_get(relative_url)


@retry_when_unauthorized
def post_request(relative_url, data):
    return http_post(relative_url, data)


@retry_when_unauthorized
def put_request(relative_url, data, headers=None):
    return http_put(relative_url, data, headers)


@retry_when_unauthorized
def delete_request(relative_url):
    return http_delete(relative_url)
