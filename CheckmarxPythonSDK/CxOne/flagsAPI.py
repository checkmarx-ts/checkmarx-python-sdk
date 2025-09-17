from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .utilities import type_check, list_member_type_check
from .dto import (
    Flag, construct_feature_flag,
)
from typing import List

api_url = f"/api/flags/"


def __construct_flag(flag):
    return Flag(
        name=flag.get("name"),
        status=flag.get("status"),
        payload=flag.get("payload")
    )


class FeatureFlagAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_all_feature_flags(self, ids: List[str] = None) -> List[Flag]:
        """
        Args:
             ids (`list`) (comma separated)

        Returns:
            `list` of `Flag`
        """
        type_check(ids, (list, tuple))
        list_member_type_check(ids, str)
        relative_url = api_url
        params = {"ids": ",".join(ids)} if ids else None
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        item = response.json()
        return [construct_feature_flag(flag) for flag in item]

    def get_feature_flag(self, name: str) -> Flag:
        """

        Args:
            name (`str`)

        Returns:
            `Flag`
        """
        type_check(name, str)
        relative_url = f"{api_url}{name}"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_feature_flag(item)


def get_all_feature_flags(ids: List[str] = None) -> List[Flag]:
    return FeatureFlagAPI().get_all_feature_flags(ids=ids)


def get_feature_flag(name: str) -> Flag:
    return FeatureFlagAPI().get_feature_flag(name=name)
