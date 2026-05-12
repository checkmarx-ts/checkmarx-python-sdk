from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import Flag
from typing import List


class FeatureFlagAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/flags"
        )

    def get_all_feature_flags(self, ids: List[str] = None) -> List[Flag]:
        """
        Args:
            ids (List[str]): comma separated

        Returns:
            List[Flag]
        """
        params = {"ids": ",".join(ids)} if ids else None
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        return [Flag.from_dict(f) for f in response.json()]

    def get_feature_flag(self, name: str) -> Flag:
        """
        Args:
            name (str):

        Returns:
            Flag
        """
        url = f"{self.base_url}/{name}"
        response = self.api_client.call_api(method="GET", url=url)
        return Flag.from_dict(response.json())


def get_all_feature_flags(ids: List[str] = None) -> List[Flag]:
    return FeatureFlagAPI().get_all_feature_flags(ids=ids)


def get_feature_flag(name: str) -> Flag:
    return FeatureFlagAPI().get_feature_flag(name=name)
