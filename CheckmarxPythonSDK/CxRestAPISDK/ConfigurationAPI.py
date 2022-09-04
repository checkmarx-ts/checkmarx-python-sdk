# encoding: utf-8
import json
from .httpRequests import get_request, put_request, get_headers
from CheckmarxPythonSDK.utilities.compat import OK
from .sast.configuration.dto import CxSASTConfig


class ConfigurationAPI(object):
    """
    CxSAST configuration API
    """
    @staticmethod
    def get_cx_component_configuration_settings(group, api_version="1.0"):
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
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxSASTConfig(
                    key=item.get("key"),
                    value=item.get("value"),
                    description=item.get("description")
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def update_cx_component_configuration_settings(group, key_value_list, api_version="1.0"):
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
        result = False
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
        response = put_request(relative_url=relative_url, data=put_data, headers=get_headers(api_version))
        if response.status_code == OK:
            result = True
        return result
