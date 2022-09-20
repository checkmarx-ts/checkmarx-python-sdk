# encoding: utf-8
from requests import Session
from zeep import Client, Settings
from zeep.transports import Transport

from CheckmarxPythonSDK.CxRestAPISDK.config import config
from . import authHeaders


def get_client_and_factory(relative_web_interface_url):
    """

    Returns:

    """

    settings = Settings(strict=False, force_https=False, extra_http_headers=authHeaders.auth_headers)

    session = Session()
    session.verify = False
    transport = Transport(session=session)
    client = Client(
        wsdl=config.get("base_url") + relative_web_interface_url,
        transport=transport,
        settings=settings
    )

    client.transport.session.verify = False

    factory = client.type_factory("ns0")

    return client, factory


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
            if response.IsSuccesfull:
                break

            # in 9.2 and previous version message id "12563" means invalid token,
            # from 9.3, it says Invalid_Token in error message
            if not response.IsSuccesfull and \
                    ('12563' in response.ErrorMessage or 'Invalid_Token' in response.ErrorMessage):
                authHeaders.update_auth_headers()
                response = func(*args, **kwargs)
            max_try -= 1

        return response
    return retry
