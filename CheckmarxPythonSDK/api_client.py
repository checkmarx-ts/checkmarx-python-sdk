import certifi
import functools
import httpx
import ssl
import time
import typing
from typing import Callable, Union
from .configuration import Configuration
from .rate_limiter import RateLimiter
from CheckmarxPythonSDK.utilities.compat import (
    OK,
    UNAUTHORIZED,
    NO_CONTENT,
    CREATED,
    ACCEPTED,
)


def create_session(configuration: Configuration) -> httpx.Client:
    raw_verify = configuration.verify
    if isinstance(raw_verify, str):
        raw_verify = False if raw_verify.lower() == "false" else (True if raw_verify.lower() == "true" else raw_verify)
    if raw_verify is False:
        verify = False
    else:
        ctx = ssl.create_default_context()
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.maximum_version = ssl.TLSVersion.TLSv1_3
        if raw_verify is True:
            ctx.load_verify_locations(certifi.where())
        else:
            ctx.load_verify_locations(raw_verify)
        verify = ctx
    return httpx.Client(
        cert=configuration.cert,
        proxy=configuration.proxy,
        transport=httpx.HTTPTransport(retries=3, verify=verify),
    )


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


def retry():
    """
    Decorator that retries the HTTP request when receiving a 401 Unauthorized or 429 Too Many Requests response.
    Uses self.configuration.max_retries to determine the retry count.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            max_retries = self.configuration.max_retries
            retries = 0
            last_exception = None

            while retries <= max_retries:
                try:
                    headers = dict(kwargs.get("headers", {}) or {})
                    token = self.token_manager.get_token()
                    headers["Authorization"] = f"Bearer {token}"
                    kwargs["headers"] = headers

                    response = func(self, *args, **kwargs)

                    if hasattr(response, "status_code"):
                        if response.status_code == 401:
                            if retries < max_retries:
                                self.token_manager.refresh_token()
                                retries += 1
                                continue
                            else:
                                response.raise_for_status()
                        elif response.status_code in (500, 502, 503, 504):
                            if retries < max_retries:
                                retries += 1
                                continue
                            else:
                                response.raise_for_status()
                        elif response.status_code == 429:
                            if retries < max_retries:
                                # Handle rate limiting
                                backoff_time = None
                                # 1. Try to get Retry-After header first
                                if response.headers.get("Retry-After"):
                                    retry_after = response.headers["Retry-After"]
                                    try:
                                        # If it's a number of seconds
                                        backoff_time = int(retry_after)
                                    except ValueError:
                                        # If it's a GMT date string, parse it
                                        from email.utils import parsedate_to_datetime

                                        retry_date = parsedate_to_datetime(retry_after)
                                        import datetime

                                        backoff_time = (
                                            retry_date
                                            - datetime.datetime.now(
                                                datetime.timezone.utc
                                            )
                                        ).total_seconds()
                                        backoff_time = max(
                                            1, backoff_time
                                        )  # Ensure at least 1 second

                                # 2. If no Retry-After, use exponential backoff
                                if backoff_time is None:
                                    # Initial wait: 60 seconds (1 minute), max wait: 300 seconds (5 minutes)
                                    base_wait = 60
                                    max_wait = 300
                                    backoff_time = min(
                                        base_wait * (2**retries), max_wait
                                    )

                                print(
                                    f"Rate limited (429), waiting {backoff_time:.2f} seconds before retrying..."
                                )
                                time.sleep(backoff_time)
                                retries += 1
                                continue
                            else:
                                response.raise_for_status()

                    return response

                except Exception as e:
                    print(f"error: {e}")
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
        method in ["GET", "HEAD"] and status_code not in [OK, UNAUTHORIZED],
        method == "POST"
        and status_code not in [OK, NO_CONTENT, CREATED, UNAUTHORIZED, ACCEPTED],
        method in ["PUT", "PATCH", "DELETE"]
        and status_code not in [OK, NO_CONTENT, ACCEPTED, UNAUTHORIZED],
    ]:
        raise ValueError(
            "HttpStatusCode: {code}".format(code=status_code),
            "ErrorMessage: {msg}".format(msg=text),
        )


class ApiClient:
    def __init__(self, configuration: Configuration = None, url_prefix: str = ""):
        self.configuration = configuration
        self.session = create_session(configuration=configuration)
        self.token_req_data = create_token_request_data(configuration=configuration)
        self.token_manager = TokenManager(token_refresh_func=self.refresh_token)
        self.url_prefix = url_prefix

        # Initialize rate limiter with configuration values
        capacity = configuration.rate_limit_capacity
        if configuration.rate_limit_refill_rate:
            refill_rate = configuration.rate_limit_refill_rate
        else:
            # Calculate refill rate if not provided
            refill_rate = capacity / configuration.rate_limit_period
        self.rate_limiter = RateLimiter(capacity=capacity, refill_rate=refill_rate)

    def refresh_token(self):
        auth_response = self.session.post(
            url=self.configuration.token_url,
            data=self.token_req_data,
            timeout=self.configuration.timeout,
        )
        auth_response.raise_for_status()
        return auth_response.json()["access_token"]

    @retry()
    def call_api(
        self,
        method: str,
        url: str,
        params: dict = None,
        data=None,
        files=None,
        json: Union[typing.Any, None] = None,
        auth=None,
        headers: dict = None,
    ):
        # Acquire token for rate limiting
        if not self.rate_limiter.acquire():
            raise RuntimeError("Rate limiter failed to acquire token")

        if params:
            params = {k: v for k, v in params.items() if v is not None}

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            files=files,
            json=json,
            auth=auth,
            timeout=self.configuration.timeout,
            headers=headers,
        )
        check_response(response)
        return response

    def head_request(self, url, auth=None, headers=None, json=None, params=None):
        return self.call_api(method="HEAD", url=url, auth=auth, headers=headers, json=json, params=params)

    def get_request(self, url, auth=None, headers=None, params=None):
        return self.call_api(method="GET", url=url, auth=auth, headers=headers, params=params)

    def post_request(self, url, data=None, files=None, auth=None, headers=None, params=None, json=None):
        return self.call_api(method="POST", url=url, data=data, files=files, auth=auth, headers=headers, params=params, json=json)

    def put_request(self, url, data=None, files=None, auth=None, headers=None, params=None, json=None):
        return self.call_api(method="PUT", url=url, data=data, files=files, auth=auth, headers=headers, params=params, json=json)

    def patch_request(self, url, data=None, auth=None, headers=None, params=None, json=None):
        return self.call_api(method="PATCH", url=url, data=data, auth=auth, headers=headers, params=params, json=json)

    def delete_request(self, url, data=None, auth=None, headers=None, params=None, json=None):
        return self.call_api(method="DELETE", url=url, data=data, auth=auth, headers=headers, params=params, json=json)
