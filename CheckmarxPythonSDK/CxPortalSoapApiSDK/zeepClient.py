# encoding: utf-8
from zeep import Client, Settings

from ..config import config
from . import authHeaders


def get_client_and_factory():
    """

    Returns:

    """

    settings = Settings(strict=False, force_https=False, extra_http_headers=authHeaders.auth_headers)

    c = Client(
        wsdl=config.get("base_url") + "/CxWebInterface/Portal/CxWebService.asmx?wsdl",
        settings=settings
    )

    c.transport.session.verify = False

    f = c.type_factory("ns0")

    return c, f


client, factory = get_client_and_factory()
