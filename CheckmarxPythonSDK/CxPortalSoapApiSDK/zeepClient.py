# encoding: utf-8
from zeep import Client, Settings

from ..config import config
from ..auth import get_new_token


def get_client_and_factory():
    """

    Returns:

    """
    token = get_new_token(
        base_url=config.get("base_url"),
        username=config.get("username"),
        password=config.get("password"),
        grant_type="password",
        scope="sast_api",
        client_id="resource_owner_sast_client",
        client_secret="014DF517-39D1-4453-B7B3-9930C563627C"
    )

    settings = Settings(strict=False, force_https=False, extra_http_headers={"Authorization": token})

    c = Client(
        wsdl=config.get("base_url") + "/CxWebInterface/Portal/CxWebService.asmx?wsdl",
        settings=settings
    )

    c.transport.session.verify = False

    f = c.type_factory("ns0")

    return c, f


client, factory = get_client_and_factory()
