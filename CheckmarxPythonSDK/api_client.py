import functools
import requests
from typing import Callable
from urllib3.util import Retry
from requests import Session
from requests.adapters import HTTPAdapter
from .configuration import Configuration
from CheckmarxPythonSDK.utilities.compat import (
    OK, UNAUTHORIZED, NO_CONTENT, CREATED, ACCEPTED
)


def create_session() -> Session:
    session = Session()
    session.verify = False
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods={'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD'},
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session


def create_token_request_data(configuration: Configuration) -> dict:
    # default to SAST platform
    token_req_data = {
        "username": configuration.username,
        "password": configuration.password,
        "grant_type": configuration.grant_type,
        "scope": configuration.scope,
        "client_id": configuration.client_id,
        "client_secret": configuration.client_secret,
    }
    # CxOne platform
    if "iam.checkmarx.net" in configuration.token_url:
        token_req_data = {
            "grant_type": "client_credentials",
            "client_id": configuration.client_id,
            "client_secret": configuration.client_secret,
        }
        if configuration.grant_type == "refresh_token":
            token_req_data = {
                "grant_type": "refresh_token",
                "client_id": "ast-app",
                "refresh_token": configuration.api_key,
            }
    # SCA platform
    if "platform.checkmarx.net" in configuration.token_url:
        token_req_data = {
            "username": configuration.username,
            "password": configuration.password,
            "acr_values": "Tenant:" + str(configuration.tenant_name),
            "grant_type": "password",
            "scope": configuration.scope,
            "client_id": "sca_resource_owner",
        }
    return token_req_data


class TokenManager:
    def __init__(self, token_refresh_func: Callable[..., str], *args, **kwargs):
        self.token_refresh_func = token_refresh_func
        self.args = args
        self.kwargs = kwargs
        self.current_token = None

    def get_token(self) -> str:
        if self.current_token is None:
            self.refresh_token()
        return self.current_token

    def refresh_token(self) -> None:
        self.current_token = self.token_refresh_func(*self.args, **self.kwargs)


def retry_when_unauthorized(max_retries: int = 1):
    """
    Decorator that retries the HTTP request when receiving a 401 Unauthorized response.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            retries = 0
            last_exception = None

            while retries <= max_retries:
                try:
                    token = self.token_manager.get_token()

                    headers = kwargs.get('headers', {})
                    headers['Authorization'] = f'Bearer {token}'
                    kwargs['headers'] = headers

                    response = func(self, *args, **kwargs)

                    if hasattr(response, 'status_code') and response.status_code == 401:
                        if retries < max_retries:
                            self.token_manager.refresh_token()
                            retries += 1
                            continue
                        else:
                            response.raise_for_status()

                    return response

                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 401 and retries < max_retries:
                        self.token_manager.refresh_token()
                        retries += 1
                        last_exception = e
                        continue
                    raise

                except Exception as e:
                    raise

            if last_exception:
                raise last_exception
            raise Exception("Max retries exceeded")

        return wrapper

    return decorator


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


class ApiClient(object):
    def __init__(self, configuration: Configuration = None, url_prefix: str = ""):
        self.configuration = configuration
        self.session = create_session()
        self.token_req_data = create_token_request_data(configuration)
        self.token_manager = TokenManager(self.refresh_token)
        self.url_prefix = url_prefix

    def refresh_token(self):
        auth_response = requests.post(
            self.configuration.token_url,
            data=self.token_req_data,
            timeout=self.configuration.timeout,
            verify=self.configuration.verify_ssl_cert,
            cert=self.configuration.cert,
            proxies=self.configuration.proxies
        )
        auth_response.raise_for_status()
        return auth_response.json()["access_token"]

    def create_url(self, relative_url, is_iam) -> str:
        url = f"{self.configuration.server_base_url}{self.url_prefix}{relative_url}"
        # is_iam is used for Access Control API
        if is_iam:
            http_fqdn_list = self.configuration.token_url.split("/")[0:3]
            http_fqdn_list.pop(1)
            access_control_url = "//".join(http_fqdn_list)
            url = access_control_url + relative_url
        return url

    def head(self, url, auth=None, headers=(), json=None, params=None):
        response = self.session.request(
            "HEAD", url, params=params, json=json, auth=auth,
            timeout=self.configuration.timeout,
            headers=headers, verify=self.configuration.verify_ssl_cert, cert=self.configuration.cert,
            proxies=self.configuration.proxies
        )
        check_response(response)
        return response

    def get(self, url, auth=None, headers=(), params=None):
        response = self.session.request(
            "GET", url, params=params, auth=auth,
            timeout=self.configuration.timeout,
            headers=headers, verify=self.configuration.verify_ssl_cert, cert=self.configuration.cert,
            proxies=self.configuration.proxies
        )
        check_response(response)
        return response

    def post(self, url, data=None, files=None, auth=None, headers=(), params=None, json=None):
        response = self.session.request(
            "POST", url, params=params, files=files, data=data, json=json, auth=auth,
            timeout=self.configuration.timeout,
            headers=headers, verify=self.configuration.verify_ssl_cert, cert=self.configuration.cert,
            proxies=self.configuration.proxies
        )
        check_response(response)
        return response

    def put(self, url, data=None, files=None, auth=None, headers=(), params=None, json=None):
        response = self.session.request(
            "PUT", url, params=params, files=files, data=data, json=json, auth=auth,
            timeout=self.configuration.timeout,
            headers=headers, verify=self.configuration.verify_ssl_cert, cert=self.configuration.cert,
            proxies=self.configuration.proxies
        )
        check_response(response)
        return response

    def patch(self, url, data=None, auth=None, headers=(), params=None, json=None):
        response = self.session.request(
            "PATCH", url, params=params, data=data, json=json, auth=auth,
            timeout=self.configuration.timeout,
            headers=headers, verify=self.configuration.verify_ssl_cert, cert=self.configuration.cert,
            proxies=self.configuration.proxies
        )
        check_response(response)
        return response

    def delete(self, url, data=None, auth=None, headers=(), params=None):
        response = self.session.request(
            "DELETE", url, params=params, data=data, auth=auth,
            timeout=self.configuration.timeout,
            headers=headers, verify=self.configuration.verify_ssl_cert, cert=self.configuration.cert,
            proxies=self.configuration.proxies
        )
        check_response(response)
        return response

    @retry_when_unauthorized(max_retries=2)
    def head_request(self, relative_url, auth=None, headers=(), json=None, params=None, is_iam=False):
        url = self.create_url(relative_url=relative_url, is_iam=is_iam)
        return self.head(url=url, auth=auth, headers=headers, json=json, params=params)

    @retry_when_unauthorized(max_retries=2)
    def get_request(self, relative_url, auth=None, headers=(), params=None, is_iam=False):
        url = self.create_url(relative_url=relative_url, is_iam=is_iam)
        return self.get(url=url, auth=auth, headers=headers, params=params)

    @retry_when_unauthorized(max_retries=2)
    def post_request(self, relative_url, data=None, files=None, auth=None, headers=(), params=None, json=None,
                     is_iam=False):
        url = self.create_url(relative_url=relative_url, is_iam=is_iam)
        return self.post(url=url, data=data, files=files, auth=auth, headers=headers, params=params, json=json)

    @retry_when_unauthorized(max_retries=2)
    def put_request(
            self, relative_url, data=None, files=None, auth=None, headers=(), params=None, json=None, is_iam=False
    ):
        url = self.create_url(relative_url=relative_url, is_iam=is_iam)
        return self.put(url=url, data=data, files=files, auth=auth, headers=headers, params=params, json=json)

    @retry_when_unauthorized(max_retries=2)
    def patch_request(self, relative_url, data=None, auth=None, headers=(), params=None, json=None, is_iam=False):
        url = self.create_url(relative_url=relative_url, is_iam=is_iam)
        return self.patch(url=url, data=data, auth=auth, headers=headers, params=params, json=json)

    @retry_when_unauthorized(max_retries=2)
    def delete_request(self, relative_url, data=None, auth=None, headers=(), params=None, is_iam=False):
        url = self.create_url(relative_url=relative_url, is_iam=is_iam)
        return self.delete(url=url, data=data, auth=auth, headers=headers, params=params)
