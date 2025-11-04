from typing import List, Union
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration, get_headers
import json
from CheckmarxPythonSDK.utilities.compat import OK
from .sast.configuration.dto import CxSASTConfig


class ConfigurationAPI(object):
    """
    CxSAST configuration API
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_cx_component_configuration_settings(self, group: str, api_version: str = "1.0") -> List[CxSASTConfig]:
        """

        Args:
            group (str):
            api_version (str, optional):

            ID Name                       Description
            0  None                       N/A
            1  AppSecCoach                N/A
            2  AuthorizationService       N/A
            3  Portal                     The CxSAST Portal
            4  Scanning                   Scans Settings
            5  SystemSettings             System wide settings
            6  QueueSettings              Specific settings around the scanning queue
            7  Audit                      Setting for the CxAudit
            8  Logging                    Logs related settings
            9  DataRetention              Data retention related settings
            10 Reports                    Reports settings
        Returns:
            list of `CxSASTConfig`
        """
        result = []
        relative_url = "/cxrestapi/configurationsExtended/{group}".format(group=group)
        response = self.api_client.get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxSASTConfig(
                    key=item.get("key"),
                    value=item.get("value"),
                    description=item.get("description")
                ) for item in response.json()
            ]
        return result

    def update_cx_component_configuration_settings(
            self, group: str, key_value_list: Union[List[dict], List[CxSASTConfig]], api_version: str = "1.0"
    ) -> bool:
        """

        Warnings: Depending on the changed settings, in order to take effect,
        corresponding SAST services should be restarted.

        Args:
            group (str): example, SystemSettings
            key_value_list (`list` of `dict`, `list` of `CxSASTConfig`）: example, [
                  {
                    "key": "MAXIMUM_CONCURRENT_SCAN_EXECUTERS",
                    "value": "2"
                  }
                ]
            api_version (str, optional):

        Returns:
            bool
        """
        relative_url = "/cxrestapi/configurationsExtended/{group}".format(group=group)

        temp_list = []
        for item in key_value_list:
            if isinstance(item, dict):
                temp_list.append(item)
            elif isinstance(item, CxSASTConfig):
                temp_list.append(item.get_key_value_dict())

        put_data = json.dumps([
            {
                "key": item.get("key"),
                "value": item.get("value"),
            } for item in temp_list
        ])
        response = self.api_client.put_request(
            relative_url=relative_url, data=put_data, headers=get_headers(api_version)
        )
        return response.status_code == OK
