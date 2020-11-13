# encoding: utf-8
from requests import Session
from zeep import Client, Settings
from zeep.transports import Transport

from ..config import config
from . import authHeaders


def get_client_and_factory():
    """

    Returns:

    """

    settings = Settings(strict=False, force_https=False, extra_http_headers=authHeaders.auth_headers)

    session = Session()
    session.verify = False
    transport = Transport(session=session)
    c = Client(
        wsdl=config.get("base_url") + "/CxWebInterface/Portal/CxWebService.asmx?wsdl",
        transport=transport,
        settings=settings
    )

    c.transport.session.verify = False

    f = c.type_factory("ns0")

    return c, f


client, factory = get_client_and_factory()
