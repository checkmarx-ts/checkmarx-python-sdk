# encoding: utf-8
# For REST API, using Python requests package to initiate the requests, and get response
import requests
from CheckmarxPythonSDK.utilities.compat import (
    OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, FORBIDDEN, NO_CONTENT, CREATED, ACCEPTED
)
from CheckmarxPythonSDK.utilities.CxError import BadRequestError, NotFoundError, CxError
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)


def request(method, url, params=None, data=None, json=None, files=None, auth=None, timeout=None, headers=None,
            verify=False, cert=None):
    """
    https://requests.readthedocs.io/en/latest/api/#requests.request
    Args:
        method (str): method for the new Request object: GET, OPTIONS, HEAD, POST, PUT, PATCH, or DELETE.
        url (str):
        params (dict):
        data (dict, optional): Dictionary, list of tuples, bytes, or file-like object to send in the body of the
            Request.
        json (object):
        files (dict): Dictionary of 'name': file-like-objects (or {'name': file-tuple}) for multipart encoding upload.
            file-tuple can be a 2-tuple ('filename', fileobj), 3-tuple ('filename', fileobj, 'content_type') or a
            4-tuple ('filename', fileobj, 'content_type', custom_headers), where 'content-type' is a string defining
            the content type of the given file and custom_headers a dict-like object containing additional headers to
            add for the file.
        auth:
        timeout (float, tuple, optional): How many seconds to wait for the server to send data before giving up, as a
            float, or a (connect timeout, read timeout) tuple.
        headers (dict):
        verify (bool, str, optional): Either a boolean, in which case it controls whether we verify the server’s TLS
                certificate, or a string, in which case it must be a path to a CA bundle to use. Defaults to True.
                When set to False, requests will accept any TLS certificate presented by the server, and will ignore
                hostname mismatches and/or expired certificates, which will make your application vulnerable to
                man-in-the-middle (MitM) attacks. Setting verify to False may be useful during local development or
                testing.
        cert (str, tuple, optional): if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.

    Returns:

    """
    return requests.request(method=method, url=url, params=params, data=data, json=json, files=files, auth=auth,
                            timeout=timeout, headers=headers, verify=verify, cert=cert)


def get(url, data=None, auth=None, timeout=None, headers=None, verify=False, cert=None):
    """

    Args:
        url (str):
        data :
        auth :
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):

    Returns:

    """
    return request("GET", url, data=data, auth=auth, timeout=timeout, headers=headers, verify=verify, cert=cert)


def post(url, data, auth=None, timeout=None, headers=None, verify=False, cert=None):
    """

    Args:
        url (str):
        data (dict):
        auth :
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):

    Returns:
    """
    return request("POST", url, data=data, auth=auth, timeout=timeout, headers=headers, verify=verify, cert=cert)


def put(url, data, auth=None, timeout=None, headers=None, verify=False, cert=None):
    """

    Args:
        url (str):
        data (dict, BinaryIO, StringIO):
        auth :
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):

    Returns:
    """
    return request("PUT", url, data=data, auth=auth, timeout=timeout, headers=headers, verify=verify, cert=cert)


def patch(url, data, auth=None, timeout=None, headers=None, verify=False, cert=None):
    """

    Args:
        url (str):
        data (dict):
        auth :
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):

    Returns:
    """
    return request("PATCH", url, auth=auth, data=data, timeout=timeout, headers=headers, verify=verify, cert=cert)


def delete(url, data=None, auth=None, timeout=None, headers=None, verify=False, cert=None):
    """

    Args:
        url (str):
        data:
        auth:
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):

    Returns:

    """
    return request("DELETE", url, data=data, auth=auth, timeout=timeout, headers=headers, verify=verify, cert=cert)


def get_new_token(token_url, request_data, timeout=None, verify_ssl_cert=False, cert=None):
    """

    Args:
        token_url (str): "http://localhost"
        request_data (dict):
        timeout (float, tuple, optional):
        verify_ssl_cert (bool, str):
        cert:

    Returns:
        Bear Token (str)
    """

    response = post(url=token_url, data=request_data, timeout=timeout, verify=verify_ssl_cert, cert=cert)

    if response.status_code != OK:
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")


def get_new_header(token_url, req_data, timeout=None, verify_ssl_cert=False, cert=None):
    """

    Args:
        token_url (str):
        req_data (dict):
        timeout (float, tuple, optional):
        verify_ssl_cert (bool, str):
        cert:

    Returns:

    """
    new_token = get_new_token(
        token_url=token_url,
        request_data=req_data,
        timeout=timeout,
        verify_ssl_cert=verify_ssl_cert,
        cert=cert
    )
    return {
        "Authorization": new_token,
        "Accept": "application/json;v=1.0",
        "Content-Type": "application/json;v=1.0",
    }


def get_header_closure():
    url = None
    auth_header = {
        "Authorization": None,
        "Accept": "application/json;v=1.0",
        "Content-Type": "application/json;v=1.0",
    }

    def inner_func(token_url, req_data, timeout=None, verify_ssl_cert=False, cert=None, token_expired=False):
        nonlocal url
        nonlocal auth_header
        if not token_expired and token_url == url:
            return auth_header
        url = token_url
        new_header = get_new_header(token_url, req_data, timeout, verify_ssl_cert, cert)
        auth_header.update(new_header)
        return auth_header

    return inner_func


get_header_func = get_header_closure()


def retry_when_unauthorized(function_to_send_request, data, get_data_from_config, relative_url, auth=None, headers=()):
    server_url, token_url, timeout, verify, cert, token_req_data = get_data_from_config()
    url = server_url + relative_url
    origin_headers = get_header_func(token_url, token_req_data, timeout, verify, cert)
    origin_headers.update(headers)
    response = function_to_send_request(url, data, auth, timeout, origin_headers, verify=verify, cert=cert)
    if UNAUTHORIZED == response.status_code:
        new_auth_header = get_header_func(token_url, token_req_data, timeout, verify, cert, token_expired=True)
        new_auth_header.update(headers)
        response = function_to_send_request(url, data, auth, timeout, new_auth_header, verify=verify, cert=cert)
    return response


def http_get(get_data_from_config, relative_url, auth=None, headers=()):
    return retry_when_unauthorized(
        function_to_send_request=get,
        data=None,
        get_data_from_config=get_data_from_config,
        relative_url=relative_url,
        auth=auth,
        headers=headers,
    )


def http_post(data, get_data_from_config, relative_url, auth=None, headers=()):
    return retry_when_unauthorized(
        function_to_send_request=post,
        data=data,
        get_data_from_config=get_data_from_config,
        relative_url=relative_url,
        auth=auth,
        headers=headers,
    )


def http_put(data, get_data_from_config, relative_url, auth=None, headers=()):
    return retry_when_unauthorized(
        function_to_send_request=put,
        data=data,
        get_data_from_config=get_data_from_config,
        relative_url=relative_url,
        auth=auth,
        headers=headers,
    )


def http_patch(data, get_data_from_config, relative_url, auth=None, headers=()):
    return retry_when_unauthorized(
        function_to_send_request=patch,
        data=data,
        get_data_from_config=get_data_from_config,
        relative_url=relative_url,
        auth=auth,
        headers=headers,
    )


def http_delete(get_data_from_config, relative_url, data=None, auth=None, headers=()):
    return retry_when_unauthorized(
        function_to_send_request=delete,
        data=data,
        get_data_from_config=get_data_from_config,
        relative_url=relative_url,
        auth=auth,
        headers=headers,
    )


def build_request_funcs(get_data_from_config):
    def get_request(relative_url, auth=None, headers=()):
        return http_get(get_data_from_config, relative_url, auth=auth, headers=headers)

    def post_request(relative_url, data, auth=None, headers=()):
        return http_post(data, get_data_from_config, relative_url, auth=auth, headers=headers)

    def put_request(relative_url, data, auth=None, headers=()):
        return http_put(data, get_data_from_config, relative_url, auth=auth, headers=headers)

    def patch_request(relative_url, data, auth=None, headers=()):
        return http_patch(data, get_data_from_config, relative_url, auth=auth, headers=headers)

    def delete_request(relative_url, data=None, auth=None, headers=()):
        return http_delete(get_data_from_config, relative_url, data=data, auth=auth, headers=headers)

    return get_request, post_request, put_request, patch_request, delete_request


def check_response(response):
    method = response.request.method
    status_code = response.status_code
    text = response.text
    if True in [
        method == 'GET' and status_code not in [OK, UNAUTHORIZED],
        method == 'POST' and status_code not in [OK, CREATED, UNAUTHORIZED],
        method in ['PUT', 'PATCH', 'DELETE'] and status_code not in [OK, NO_CONTENT, ACCEPTED, UNAUTHORIZED],
    ]:
        raise ValueError("HttpStatusCode: {code}".format(code=status_code),
                         "ErrorMessage: {msg}".format(msg=text))


def check_response_status_code(response):
    """
    Just to be backward compatible with old code.
    Args:
        response:

    Returns:

    """
    status_code = response.status_code
    if status_code in [OK, CREATED, NO_CONTENT, ACCEPTED]:
        return
    elif status_code == BAD_REQUEST:
        raise BadRequestError(response.text)
    elif status_code == NOT_FOUND:
        raise NotFoundError()
    else:
        raise CxError(response.text, status_code)
