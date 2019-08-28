# encoding: utf-8
import http

import requests

from ...config import CxConfig
from ...auth import AuthenticationAPI
from ...exceptions.CxError import BadRequestError, NotFoundError, UnknownHttpStatusError
from .dto.customFields import CxCustomField


class CustomFieldsAPI(object):
    """

    """
    max_try = CxConfig.CxConfig.config.max_try
    custom_fields = []
    custom_fields_url = CxConfig.CxConfig.config.url + "/customFields"

    def __init__(self):
        """

        """
        self.retry = 0

    def get_all_custom_fields(self):
        """
        REST API: get all custom fields

        Returns:
            :obj:`list` of :obj:`CxTeam` :

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        custom_fields = []

        r = requests.get(url=CustomFieldsAPI.custom_fields_url,
                         headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == http.HTTPStatus.OK:
            a_list = r.json()
            custom_fields = [
                CxCustomField.CxCustomField(
                    custom_field_id=item.get("id"),
                    name=item.get("name")
                ) for item in a_list
            ]
            CustomFieldsAPI.custom_fields = custom_fields
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_custom_fields()
        else:
            raise UnknownHttpStatusError()

        return custom_fields

    def get_custom_field_id_by_name(self, custom_field_name):
        """
        utility provided by SDK: get custom field id by custom field name

        Args:
            custom_field_name (str):

        Returns:
            int:  the team id for the team full name
        """
        all_custom_fields = self.get_all_custom_fields()
        # construct a dict of name: id
        custom_field_name_id_dict = {item.name: item.id for item in all_custom_fields}
        return custom_field_name_id_dict.get(custom_field_name)
