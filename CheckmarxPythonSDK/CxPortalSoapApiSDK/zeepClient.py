# encoding: utf-8
import functools
from typing import Callable
from zeep import Client, Settings
from zeep.transports import Transport
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.CxPortalSoapApiSDK.config import construct_configuration


def retry_when_unauthorized(max_retries: int = 1):
    """
    Decorator that retries the HTTP request when receiving a 401 Unauthorized response.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            retries = 0
            # last_exception = None

            while retries <= max_retries:
                response = func(self, *args, **kwargs)
                if response.IsSuccesfull:
                    return response
                # in 9.2 and previous version message id "12563" means invalid token,
                # from 9.3, it says Invalid_Token in error message
                if not response.IsSuccesfull and \
                        (response.ErrorMessage is None
                         or '12563' in response.ErrorMessage
                         or 'Invalid_Token' in response.ErrorMessage):
                    self.token_manager.refresh_token()
                retries += 1
            raise Exception("Max retries exceeded")

        return wrapper

    return decorator


class ZeepClient(ApiClient):

    def __init__(self, relative_web_interface_url, configuration: Configuration = None):
        if configuration is None:
            configuration = construct_configuration()
        ApiClient.__init__(self, configuration=configuration)
        self.client = Client(
            wsdl=f"{configuration.server_base_url}{relative_web_interface_url}",
            transport=Transport(session=self.session),
            settings=Settings(
                strict=False,
                force_https=False,
                extra_http_headers={"Authorization": f'Bearer {self.token_manager.get_token()}'}
            )
        )
        self.factory = self.client.type_factory("ns0")

    @retry_when_unauthorized(max_retries=1)
    def execute(self, operation_name: str, *args, **kwargs):
        return self.client.service[operation_name](*args, **kwargs)
