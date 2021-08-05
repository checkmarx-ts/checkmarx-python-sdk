# encoding: utf-8
import requests
import json

from ..compat import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED
from ..config import config

from . import authHeaders
from .exceptions.CxError import BadRequestError, NotFoundError, CxError
from .sast.configuration.dto import CxSASTConfig


class ConfigurationAPI(object):
    """
    CxSAST configuration API
    """
    def __init__(self):
        """

        """
        self.retry = 0

    def get_cx_component_configuration_settings(self, group, api_version="1.0"):
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
        url = config.get("base_url") + "/cxrestapi/configurationsExtended/{group}".format(group=group)

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_list = r.json()
            configurations = [
                CxSASTConfig(
                    key=item.get("key"),
                    value=item.get("value"),
                    description=item.get("description")
                ) for item in a_list
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            configurations = self.get_cx_component_configuration_settings(group, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return configurations

    def update_cx_component_configuration_settings(self, group, key_value_list, api_version="1.0"):
        """

        Warnings: Depending on the changed settings, in order to take effect,
        corresponding SAST services should be restarted.

        Args:
            group (str): example, SystemSettings
            key_value_list (list of dict）: example, [
                  {
                    "key": "MAXIMUM_CONCURRENT_SCAN_EXECUTERS",
                    "value": "2"
                  }
                ]
            api_version (str, optional):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/configurationsExtended/{group}".format(group=group)

        data = json.dumps(key_value_list)

        r = requests.put(
            url=url,
            data=data,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_cx_component_configuration_settings(group, key_value_list,
                                                                            api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful
