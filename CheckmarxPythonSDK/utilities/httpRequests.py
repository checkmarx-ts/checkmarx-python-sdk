# encoding: utf-8
# For REST API, using Python requests package to initiate the requests, and get response
import requests
import logging
from CheckmarxPythonSDK.utilities.compat import (
    OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, FORBIDDEN, NO_CONTENT, CREATED, ACCEPTED
)
from CheckmarxPythonSDK.utilities.CxError import BadRequestError, NotFoundError, CxError
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ConnectionError
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.exceptions import TransportServerError
disable_warnings(InsecureRequestWarning)

logger = logging.getLogger("CheckmarxPythonSDK")


def request(method, url, params=None, data=None, json=None, files=None, auth=None, timeout=None, headers=None,
            verify=False, cert=None, proxies=None):
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
    for _ in range(3):
        try:
            response = requests.request(method=method, url=url, params=params, data=data, json=json, files=files,
                                        auth=auth, timeout=timeout, headers=headers, verify=verify, cert=cert,
                                        proxies=proxies)
            return response
        except ConnectionError:
            logger.error("Connection error. Retrying...")


def head(url, files=None, data=None, auth=None, timeout=None, headers=None, verify=False, cert=None, proxies=None):
    """

    Args:
        url (str):
        files :
        data :
        auth :
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):
        proxies (dict, optional)

    Returns:

    """
    return request("HEAD", url, files=files, data=data, auth=auth, timeout=timeout, headers=headers,
                   verify=verify, cert=cert, proxies=proxies)


def get(url, files=None, data=None, auth=None, timeout=None, headers=None, verify=False, cert=None, proxies=None):
    """

    Args:
        url (str):
        files :
        data :
        auth :
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):
         proxies (dict, optional):

    Returns:

    """
    return request("GET", url, files=files, data=data, auth=auth, timeout=timeout, headers=headers,
                   verify=verify, cert=cert, proxies=proxies)


def post(url, data, files=None, auth=None, timeout=None, headers=None, verify=False, cert=None, proxies=None):
    """

    Args:
        url (str):
        data (dict):
        files (dict):
        auth :
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):
         proxies (dict, optional):

    Returns:
    """
    return request("POST", url, data=data, files=files, auth=auth, timeout=timeout, headers=headers,
                   verify=verify, cert=cert, proxies=proxies)


def put(url, data, files=None, auth=None, timeout=None, headers=None, verify=False, cert=None, proxies=None):
    """

    Args:
        url (str):
        data (dict, BinaryIO, StringIO):
        files (dict):
        auth :
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):
        proxies (dict, optional):

    Returns:
    """
    return request("PUT", url, data=data, files=files, auth=auth, timeout=timeout, headers=headers,
                   verify=verify, cert=cert, proxies=proxies)


def patch(url, data, files=None, auth=None, timeout=None, headers=None, verify=False, cert=None, proxies=None):
    """

    Args:
        url (str):
        data (dict):
        files :
        auth :
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):
        proxies (dict, optional):

    Returns:
    """
    return request("PATCH", url, files=files, auth=auth, data=data, timeout=timeout, headers=headers,
                   verify=verify, cert=cert, proxies=proxies)


def delete(url, data=None, files=None, auth=None, timeout=None, headers=None, verify=False, cert=None, proxies=None):
    """

    Args:
        url (str):
        data:
        files:
        auth:
        timeout (float, tuple, optional):
        headers (dict):
        verify (bool, str, optional):
        cert (str, tuple, optional):
        proxies (dict, optional)

    Returns:

    """
    return request("DELETE", url, files=files, data=data, auth=auth, timeout=timeout, headers=headers,
                   verify=verify, cert=cert, proxies=proxies)


def gql_(url, data, files=None, auth=None, timeout=None, headers=None, verify=False, cert=None, proxies=None):
    # Select your transport with a defined url endpoint
    transport = RequestsHTTPTransport(url=url, auth=auth, timeout=timeout, headers=headers, verify=verify, retries=3,
                                      cert=cert, proxies=proxies)
    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)
    query = gql(data)
    return client.execute(query)


def get_new_token(token_url, request_data, timeout=None, verify_ssl_cert=False, cert=None, proxies=None):
    """

    Args:
        token_url (str): "http://localhost"
        request_data (dict):
        timeout (float, tuple, optional):
        verify_ssl_cert (bool, str):
        cert:
        proxies (dict, optional):

    Returns:
        Bear Token (str)
    """

    response = post(url=token_url, data=request_data, timeout=timeout, verify=verify_ssl_cert, cert=cert,
                    proxies=proxies)

    if response.status_code != OK:
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")


def update_header(token_url, req_data, timeout=None, verify_ssl_cert=False, cert=None, proxies=None):
    """

    Args:
        token_url (str):
        req_data (dict):
        timeout (float, tuple, optional):
        verify_ssl_cert (bool, str):
        cert:
        proxies (dict, optional)

    Returns:

    """
    new_token = get_new_token(
        token_url=token_url,
        request_data=req_data,
        timeout=timeout,
        verify_ssl_cert=verify_ssl_cert,
        cert=cert,
        proxies=proxies,
    )
    auth_header.update({"Authorization": new_token})


auth_header = {
    "Authorization": None,
    "Content-Type": "application/json"
}


def retry_when_unauthorized(function_to_send_request, data, get_data_from_config, relative_url, files=None, auth=None,
                            headers=(), is_iam=False):
    server_url, token_url, timeout, verify, cert, token_req_data, proxies = get_data_from_config()
    url = server_url + relative_url
    # is_iam is used for Access Control API
    if is_iam:
        http_fqdn_list = token_url.split("/")[0:3]
        http_fqdn_list.pop(1)
        access_control_url = "//".join(http_fqdn_list)
        url = access_control_url + relative_url
    temp_header = auth_header.copy()
    if headers:
        temp_header.update(headers)
    if temp_header.get("Authorization") is None:
        update_header(token_url, token_req_data, timeout, verify, cert, proxies=proxies)
        temp_header.update(auth_header)
    logger.debug(
        "first http request:"
        "method: {method}, url: {url}, data: {data}, auth: {auth}, timeout: {timeout}, "
        "origin_headers: {origin_headers}, verify: {verify}, cert: {cert}, proxies: {proxies}".format(
            method=function_to_send_request.__name__, url=url, data=data, auth=auth, timeout=timeout,
            origin_headers=temp_header, verify=verify, cert=cert, proxies=proxies
        )
    )

    def update_token_and_try_again():
        update_header(token_url, token_req_data, timeout, verify, cert, proxies=proxies)
        temp_header.update(auth_header)
        logger.debug(
            "http response status code is UNAUTHORIZED !\n."
            "renew token, and send second http request:"
            "method: {method}, url: {url}, data: {data}, auth: {auth}, timeout: {timeout}, "
            "new_auth_header: {new_auth_header}, verify: {verify}, cert: {cert}".format(
                method=function_to_send_request.__name__, url=url, data=data, auth=auth, timeout=timeout,
                new_auth_header=temp_header, verify=verify,
                cert=cert, proxies=proxies,
            )
        )
        return function_to_send_request(url=url, data=data, auth=auth, timeout=timeout, headers=temp_header,
                                            files=files, verify=verify, cert=cert, proxies=proxies)
    try:
        response = function_to_send_request(url=url, data=data, auth=auth, timeout=timeout, headers=temp_header,
                                            files=files, verify=verify, cert=cert, proxies=proxies)
    except TransportServerError:
        return update_token_and_try_again()
    if hasattr(response, 'status_code') and UNAUTHORIZED == response.status_code:
        return update_token_and_try_again()
    return response


def build_request_funcs(get_data_from_config):

    def head_request(relative_url, auth=None, headers=(), is_iam=False):
        return retry_when_unauthorized(
            function_to_send_request=head,
            data=None,
            get_data_from_config=get_data_from_config,
            relative_url=relative_url,
            auth=auth,
            headers=headers,
            is_iam=is_iam,
        )

    def get_request(relative_url, auth=None, headers=(), is_iam=False):
        return retry_when_unauthorized(
            function_to_send_request=get,
            data=None,
            get_data_from_config=get_data_from_config,
            relative_url=relative_url,
            auth=auth,
            headers=headers,
            is_iam=is_iam,
        )

    def post_request(relative_url, data, files=None, auth=None, headers=(), is_iam=False):
        return retry_when_unauthorized(
            function_to_send_request=post,
            data=data,
            get_data_from_config=get_data_from_config,
            relative_url=relative_url,
            files=files,
            auth=auth,
            headers=headers,
            is_iam=is_iam,
        )

    def put_request(relative_url, data, files=None, auth=None, headers=(), is_iam=False):
        return retry_when_unauthorized(
            function_to_send_request=put,
            data=data,
            get_data_from_config=get_data_from_config,
            relative_url=relative_url,
            files=files,
            auth=auth,
            headers=headers,
            is_iam=is_iam,
        )

    def patch_request(relative_url, data, auth=None, headers=(), is_iam=False):
        return retry_when_unauthorized(
            function_to_send_request=patch,
            data=data,
            get_data_from_config=get_data_from_config,
            relative_url=relative_url,
            auth=auth,
            headers=headers,
            is_iam=is_iam,
        )

    def delete_request(relative_url, data=None, auth=None, headers=(), is_iam=False):
        return retry_when_unauthorized(
            function_to_send_request=delete,
            data=data,
            get_data_from_config=get_data_from_config,
            relative_url=relative_url,
            auth=auth,
            headers=headers,
            is_iam=is_iam,
        )

    def gql_request(relative_url, data=None, auth=None, headers=(), is_iam=False):
        return retry_when_unauthorized(
            function_to_send_request=gql_,
            data=data,
            get_data_from_config=get_data_from_config,
            relative_url=relative_url,
            auth=auth,
            headers=headers,
            is_iam=is_iam,
        )
    return get_request, post_request, put_request, patch_request, delete_request, head_request, gql_request


def check_response(response):
    method = response.request.method
    status_code = response.status_code
    text = response.text
    if True in [
        method in ['GET', 'HEAD'] and status_code not in [OK, UNAUTHORIZED],
        method == 'POST' and status_code not in [OK, NO_CONTENT, CREATED, UNAUTHORIZED, ACCEPTED],
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
    elif status_code == FORBIDDEN:
        raise CxError(
            response.text + " Please check the scope in your configuration file, please check if you have permission",
            status_code
        )
    else:
        raise CxError(response.text, status_code)
