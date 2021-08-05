# encoding: utf-8
import requests

from ..compat import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED
from ..config import config

from . import authHeaders
from .exceptions.CxError import BadRequestError, NotFoundError, CxError
from .sast.projects.dto import CxCustomField


class CustomFieldsAPI(object):
    """

    """

    def __init__(self):
        """

        """
        self.retry = 0

    def get_all_custom_fields(self, api_version="1.0"):
        """
        REST API: get all custom fields

        Args:
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxTeam` :

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        custom_fields_url = config.get("base_url") + "/cxrestapi/customFields"

        r = requests.get(
            url=custom_fields_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            custom_fields = [
                CxCustomField(
                    custom_field_id=item.get("id"),
                    name=item.get("name")
                ) for item in a_list
            ]
            CustomFieldsAPI.custom_fields = custom_fields
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            custom_fields = self.get_all_custom_fields(api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

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
