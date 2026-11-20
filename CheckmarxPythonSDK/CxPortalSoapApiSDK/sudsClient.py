# encoding: utf-8
import functools
from io import BytesIO
from typing import Callable
from suds.client import Client
from suds.transport import Transport, Reply
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.CxPortalSoapApiSDK.config import construct_configuration


class _RequestsTransport(Transport):
    """suds transport backed by an httpx.Client."""

    def __init__(self, session):
        super().__init__()
        self.session = session

    def open(self, request):
        response = self.session.get(request.url)
        return BytesIO(response.content)

    def send(self, request):
        response = self.session.post(
            request.url,
            content=request.message,
            headers=dict(request.headers),
        )
        return Reply(response.status_code, response.headers, response.content)


class _SudsFactory:
    """
    Wraps suds client.factory to provide zeep-compatible constructor-style
    type creation:
      factory.ComplexType(field=val, ...)  -> create object and set attributes
      factory.ArrayType([items])           -> create array wrapper and fill elements
      factory.EnumType("value")            -> return the raw value (suds accepts strings)
    """

    def __init__(self, suds_factory):
        self._f = suds_factory

    def __getattr__(self, type_name):
        f = self._f

        def creator(*args, **kwargs):
            if args and len(args) == 1 and not kwargs:
                arg = args[0]
                if isinstance(arg, list):
                    # Array wrapper type: assign the list to the first child field
                    obj = f.create(type_name)
                    fields = getattr(obj, "__keylist__", [])
                    if fields:
                        setattr(obj, fields[0], arg)
                    return obj
                # Enum or simple scalar – suds accepts the raw value directly
                return arg
            obj = f.create(type_name)
            for key, value in kwargs.items():
                setattr(obj, key, value)
            return obj

        return creator


def retry(max_retries: int = 1):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            retries = 0
            while retries <= max_retries:
                response = func(self, *args, **kwargs)
                if response.IsSuccesfull:
                    return response
                # in 9.2 and previous version message id "12563" means invalid token,
                # from 9.3, it says Invalid_Token in error message
                error_msg = getattr(response, "ErrorMessage", None)
                is_token_error = error_msg is not None and (
                    "12563" in error_msg or "Invalid_Token" in error_msg
                )
                if not response.IsSuccesfull and not is_token_error:
                    return response
                if not response.IsSuccesfull and is_token_error:
                    self.token_manager.refresh_token()
                    self.session.headers["Authorization"] = (
                        f"Bearer {self.token_manager.get_token()}"
                    )
                retries += 1
            raise Exception("Max retries exceeded")

        return wrapper

    return decorator


class SudsClient(ApiClient):

    def __init__(self, relative_web_interface_url, configuration: Configuration = None):
        if configuration is None:
            configuration = construct_configuration()
        ApiClient.__init__(self, configuration=configuration)
        self.session.headers["Authorization"] = (
            f"Bearer {self.token_manager.get_token()}"
        )
        wsdl_url = f"{configuration.server_base_url}{relative_web_interface_url}"
        self._client = Client(
            wsdl_url,
            transport=_RequestsTransport(self.session),
        )
        self._client.options.allowUnknownMessageParts = True
        self.factory = _SudsFactory(self._client.factory)

    @retry(max_retries=2)
    def execute(self, operation_name: str, *args, **kwargs):
        return getattr(self._client.service, operation_name)(*args, **kwargs)
