from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration, get_headers
from CheckmarxPythonSDK.utilities.compat import OK
from .sast.projects.dto import CxCustomField


class CustomFieldsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_all_custom_fields(self, api_version: str = "5.0") -> List[CxCustomField]:
        """
        REST API: get all custom fields

        Args:
            api_version (str, optional):

        Returns:

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = []
        relative_url = "/cxrestapi/customFields"
        response = self.api_client.get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxCustomField(
                    custom_field_id=item.get("id"),
                    name=item.get("name"),
                    is_mandatory=item.get("isMandatory")
                ) for item in response.json()
            ]
        return result

    def get_custom_field_id_by_name(self, custom_field_name: str) -> int:
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
