# encoding: utf-8

from .httpRequests import get_request, get_headers
from CheckmarxPythonSDK.utilities.compat import OK
from .sast.projects.dto import CxCustomField


class CustomFieldsAPI(object):
    """

    """
    @staticmethod
    def get_all_custom_fields(api_version="1.0"):
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
        result = []
        relative_url = "/cxrestapi/customFields"
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxCustomField(
                    custom_field_id=item.get("id"),
                    name=item.get("name")
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_custom_field_id_by_name(custom_field_name):
        """
        utility provided by SDK: get custom field id by custom field name

        Args:
            custom_field_name (str):

        Returns:
            int:  the team id for the team full name
        """
        all_custom_fields = CustomFieldsAPI.get_all_custom_fields()
        # construct a dict of name: id
        custom_field_name_id_dict = {item.name: item.id for item in all_custom_fields}
        return custom_field_name_id_dict.get(custom_field_name)
