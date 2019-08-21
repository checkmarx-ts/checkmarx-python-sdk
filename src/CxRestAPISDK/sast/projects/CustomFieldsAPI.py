# encoding: utf-8
import http

import requests

from src.CxRestAPISDK.config import CxConfig
from src.CxRestAPISDK.auth import AuthenticationAPI

from src.CxRestAPISDK.sast.projects.dto.customFields import CxCustomFields


class CustomFieldsAPI(object):
    """

    """
    custom_fields = []
    custom_fields_url = CxConfig.CxConfig.config.url + "/customFields"

    def __init__(self):
        """

        """
        self.retry = 0

    def get_all_custom_fields(self):
        """
        REST API: get all custom fields
        :return:
        list of CxTeam
        """
        custom_fields = []
        r = requests.get(url=CustomFieldsAPI.custom_fields_url,
                         headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == http.HTTPStatus.OK:
            a_list = r.json()
            custom_fields = [
                CxCustomFields.CxCustomFields(
                    id=item.get("id"),
                    name=item.get("name")
                ) for item in a_list
            ]
            CustomFieldsAPI.custom_fields = custom_fields
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise Exception("Not Found")
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < 3):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_custom_fields()
        else:
            raise Exception("Network Error")
        return custom_fields

    def get_custom_field_id_by_name(self, custom_field_name):
        """
        utility provided by SDK: get custom field id by custom field name
        :param custom_field_name: str
            custom_field_name is unique.
        :return:
        int
            the team id for the team full name
        """
        all_custom_fields = self.get_all_custom_fields()
        # construct a dict of name: id
        custom_field_name_id_dict = {item.name: item.id for item in all_custom_fields}
        return custom_field_name_id_dict.get(custom_field_name)
