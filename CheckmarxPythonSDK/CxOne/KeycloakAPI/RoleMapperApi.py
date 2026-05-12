from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.MappingsRepresentation import MappingsRepresentation
from .dto.RoleRepresentation import RoleRepresentation
from .api_url import api_url


class RoleMapperApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = f"{api_client.configuration.iam_base_url.rstrip('/')}{api_url}"

    def get_group_role_mappings(self, realm: str, id: str) -> MappingsRepresentation:
        """
        Get role mappings

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            MappingsRepresentation

        URL:
            Relative path: /{realm}/groups/{id}/role-mappings
        """
        url = f"{self.base_url}/{realm}/groups/{id}/role-mappings"
        response = self.api_client.call_api("GET", url)
        return MappingsRepresentation.from_dict(response.json())

    def get_group_role_mappings_realm(
        self, realm: str, id: str
    ) -> List[RoleRepresentation]:
        """
        Get realm-level role mappings

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            List[RoleRepresentation]

        URL:
            Relative path: /{realm}/groups/{id}/role-mappings/realm
        """
        url = f"{self.base_url}/{realm}/groups/{id}/role-mappings/realm"
        response = self.api_client.call_api("GET", url)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_group_role_mappings_realm(
        self, realm: str, id: str, role_representations: List[RoleRepresentation]
    ) -> bool:
        """
        Add realm-level role mappings to the user

        Args:
            realm (str):  [required]
            id (str):  [required]
            role_representations (List[RoleRepresentation]): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/groups/{id}/role-mappings/realm
        """
        url = f"{self.base_url}/{realm}/groups/{id}/role-mappings/realm"
        response = self.api_client.call_api("POST", url,
            json=[
                role_representation.to_dict()
                for role_representation in role_representations
            ],
            )
        return response.status_code == 204

    def delete_group_role_mappings_realm(
        self, realm: str, id: str, role_representations: List[RoleRepresentation]
    ) -> bool:
        """
        Delete realm-level role mappings

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/groups/{id}/role-mappings/realm
        """
        url = f"{self.base_url}/{realm}/groups/{id}/role-mappings/realm"
        response = self.api_client.call_api("DELETE", url,
            json=[
                role_representation.to_dict()
                for role_representation in role_representations
            ],
            )
        return response.status_code == 204

    def get_group_role_mappings_realm_available(
        self, realm: str, id: str
    ) -> List[RoleRepresentation]:
        """
        Get realm-level roles that can be mapped

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            List[RoleRepresentation]

        URL:
            Relative path: /{realm}/groups/{id}/role-mappings/realm/available
        """
        url = f"{self.base_url}/{realm}/groups/{id}/role-mappings/realm/available"
        response = self.api_client.call_api("GET", url)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_group_role_mappings_realm_composite(
        self, realm: str, id: str, brief_representation: bool = None
    ) -> List[RoleRepresentation]:
        """
        Get effective realm-level role mappings This will recurse all composite roles to get the result.

        Args:
            realm (str):  [required]
            id (str):  [required]
            brief_representation (bool): if false, return roles with their attributes

        Returns:
            List[RoleRepresentation]

        URL:
            Relative path: /{realm}/groups/{id}/role-mappings/realm/composite
        """
        params = {"briefRepresentation": brief_representation}
        url = f"{self.base_url}/{realm}/groups/{id}/role-mappings/realm/composite"
        response = self.api_client.call_api("GET", url, params=params)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_user_role_mappings(self, realm: str, id: str) -> MappingsRepresentation:
        """
        Get role mappings

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            MappingsRepresentation

        URL:
            Relative path: /{realm}/users/{id}/role-mappings
        """
        url = f"{self.base_url}/{realm}/users/{id}/role-mappings"
        response = self.api_client.call_api("GET", url)
        return MappingsRepresentation.from_dict(response.json())

    def get_user_role_mappings_realm(
        self, realm: str, id: str
    ) -> List[RoleRepresentation]:
        """
        Get realm-level role mappings

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            List[RoleRepresentation]

        URL:
            Relative path: /{realm}/users/{id}/role-mappings/realm
        """
        url = f"{self.base_url}/{realm}/users/{id}/role-mappings/realm"
        response = self.api_client.call_api("GET", url)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_user_role_mappings_realm(
        self, realm: str, id: str, role_representations: List[RoleRepresentation]
    ) -> bool:
        """
        Add realm-level role mappings to the user

        Args:
            realm (str):  [required]
            id (str):  [required]
            role_representations (List[RoleRepresentation]): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/users/{id}/role-mappings/realm
        """
        url = f"{self.base_url}/{realm}/users/{id}/role-mappings/realm"
        response = self.api_client.call_api("POST", url,
            json=[item.to_dict() for item in role_representations],
            )
        return response.status_code == 204

    def delete_user_role_mappings_realm(
        self, realm: str, id: str, role_representations: List[RoleRepresentation]
    ) -> bool:
        """
        Delete realm-level role mappings

        Args:
            realm (str):  [required]
            id (str):  [required]
            role_representations (List[RoleRepresentation]): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/users/{id}/role-mappings/realm
        """
        url = f"{self.base_url}/{realm}/users/{id}/role-mappings/realm"
        response = self.api_client.call_api("DELETE", url,
            json=[item.to_dict() for item in role_representations],
            )
        return response.status_code == 204

    def get_user_role_mappings_realm_available(
        self, realm: str, id: str
    ) -> List[RoleRepresentation]:
        """
        Get realm-level roles that can be mapped

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            List[RoleRepresentation]

        URL:
            Relative path: /{realm}/users/{id}/role-mappings/realm/available
        """
        url = f"{self.base_url}/{realm}/users/{id}/role-mappings/realm/available"
        response = self.api_client.call_api("GET", url)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_user_role_mappings_realm_composite(
        self, realm: str, id: str, brief_representation: bool = False
    ) -> List[RoleRepresentation]:
        """
        Get effective realm-level role mappings This will recurse all composite roles to get the result.

        Args:
            realm (str):  [required]
            id (str):  [required]
            brief_representation (bool): if false, return roles with their attributes

        Returns:
            List[RoleRepresentation]

        URL:
            Relative path: /{realm}/users/{id}/role-mappings/realm/composite
        """
        params = {"briefRepresentation": brief_representation}
        url = f"{self.base_url}/{realm}/users/{id}/role-mappings/realm/composite"
        response = self.api_client.call_api("GET", url, params=params)
        return [RoleRepresentation.from_dict(item) for item in response.json()]
