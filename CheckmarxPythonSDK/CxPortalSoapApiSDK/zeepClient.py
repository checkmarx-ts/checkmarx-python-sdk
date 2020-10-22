# encoding: utf-8
from zeep import Client, Settings

from .auth import config_info, get_new_token


class ZeepClient(object):
    """
    python zeep client
    """
    client = None
    factory = None

    def __init__(self):
        self.get_client_and_factory()

    @classmethod
    def get_client_and_factory(cls):
        """

        Returns:

        """
        token = get_new_token()

        settings = Settings(strict=False, force_https=False, extra_http_headers={"Authorization": token})

        client = Client(
            wsdl=config_info.get("base_url") + "/CxWebInterface/Portal/CxWebService.asmx?wsdl",
            settings=settings
        )

        client.transport.session.verify = False

        factory = client.type_factory("ns0")

        ZeepClient.client = client

        ZeepClient.factory = factory

        return ZeepClient.client, ZeepClient.factory


ZeepClient()
