# encoding: utf-8
from zeep import Client, Settings

from ..auth import config, get_new_token


def get_client_and_factory():
    """

    Returns:

    """
    token = get_new_token()

    settings = Settings(strict=False, force_https=False, extra_http_headers={"Authorization": token})

    c = Client(
        wsdl=config.get("base_url") + "/CxWebInterface/Portal/CxWebService.asmx?wsdl",
        settings=settings
    )

    c.transport.session.verify = False

    f = c.type_factory("ns0")

    return c, f


client, factory = get_client_and_factory()
