from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.IdentityProviderMapperRepresentation import IdentityProviderMapperRepresentation
from .dto.IdentityProviderRepresentation import IdentityProviderRepresentation
from .dto.ManagementPermissionReference import ManagementPermissionReference
from .api_url import api_url


class IdentityProvidersApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def post_import_config(self, realm: str) -> Dict[str, Any]:
        """
        Import identity provider from JSON body
        
        Args:
            realm (str):  [required]
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/identity-provider/import-config
        """
        relative_url = f"{api_url}/{realm}/identity_provider/import_config"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_instances(self, realm: str, brief_representation: bool = None, first: str = None, max: str = None,
                      search: bool = None) -> List[IdentityProviderRepresentation]:
        """
        List identity providers
        
        Args:
            realm (str):  [required]
            brief_representation (bool): Boolean which defines whether brief representations are returned (default: false)
            first (str): Pagination offset
            max (str): Maximum results size (defaults to 100)
            search (bool): Filter specific providers by name. Search can be prefix (name*), contains (name) or exact ("name"). Default prefixed.
        
        Returns:
            List[IdentityProviderRepresentation]
        
        URL:
            Relative path: /{realm}/identity-provider/instances
        """
        params = {"briefRepresentation": brief_representation, "first": first, "max": max, "search": search}
        relative_url = f"{api_url}/{realm}/identity_provider/instances"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [IdentityProviderRepresentation.from_dict(item) for item in response.json()]

    def post_instances(self, realm: str, identity_provider_representation: IdentityProviderRepresentation) -> bool:
        """
        Create a new identity provider
        
        Args:
            realm (str):  [required]
            identity_provider_representation (IdentityProviderRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/identity-provider/instances
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=identity_provider_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def get_instance(self, realm: str, alias: str) -> IdentityProviderRepresentation:
        """
        Get the identity provider
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
        
        Returns:
            IdentityProviderRepresentation
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return IdentityProviderRepresentation.from_dict(response.json())

    def put_instance(self, realm: str, alias: str,
                     identity_provider_representation: IdentityProviderRepresentation) -> bool:
        """
        Update the identity provider
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
            identity_provider_representation (IdentityProviderRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=identity_provider_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def delete_instance(self, realm: str, alias: str) -> bool:
        """
        Delete the identity provider
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def get_export(self, realm: str, alias: str, format: str = None) -> bool:
        """
        Export public broker configuration for identity provider
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
            format (str): Format to use
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}/export
        """
        params = {"format": format}
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}/export"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return response.status_code == 200

    def get_instance_management_permissions(self, realm: str, alias: str) -> ManagementPermissionReference:
        """
        Return object stating whether client Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}/management/permissions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def put_instance_management_permissions(self, realm: str, alias: str,
                                            management_permission_reference: ManagementPermissionReference) -> ManagementPermissionReference:
        """
        Return object stating whether client Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
            management_permission_reference (ManagementPermissionReference): Request body data [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}/management/permissions"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=management_permission_reference.to_dict(), is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def get_mapper_types(self, realm: str, alias: str) -> bool:
        """
        Get mapper types for identity provider
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}/mapper-types
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}/mapper_types"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def get_mappers(self, realm: str, alias: str) -> List[IdentityProviderMapperRepresentation]:
        """
        Get mappers for identity provider
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
        
        Returns:
            List[IdentityProviderMapperRepresentation]
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}/mappers
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}/mappers"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [IdentityProviderMapperRepresentation.from_dict(item) for item in response.json()]

    def post_mappers(self, realm: str, alias: str,
                     identity_provider_mapper_representation: IdentityProviderMapperRepresentation) -> bool:
        """
        Add a mapper to identity provider
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
            identity_provider_mapper_representation (IdentityProviderMapperRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}/mappers
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}/mappers"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=identity_provider_mapper_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def get_mapper(self, realm: str, alias: str, id: str) -> IdentityProviderMapperRepresentation:
        """
        Get mapper by id for the identity provider
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
            id (str):  [required]
        
        Returns:
            IdentityProviderMapperRepresentation
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}/mappers/{id}
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}/mappers/{id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return IdentityProviderMapperRepresentation.from_dict(response.json())

    def put_mapper(self, realm: str, alias: str, id: str,
                   identity_provider_mapper_representation: IdentityProviderMapperRepresentation) -> bool:
        """
        Update a mapper for the identity provider
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
            id (str):  [required]
            identity_provider_mapper_representation (IdentityProviderMapperRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}/mappers/{id}
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}/mappers/{id}"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=identity_provider_mapper_representation.to_dict(), is_iam=True)
        return response.status_code == 204

    def delete_mapper(self, realm: str, alias: str, id: str) -> bool:
        """
        Delete a mapper for the identity provider
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/identity-provider/instances/{alias}/mappers/{id}
        """
        relative_url = f"{api_url}/{realm}/identity_provider/instances/{alias}/mappers/{id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_identity_provider_provider(self, realm: str, provider_id: str) -> Dict[str, Any]:
        """
        Get the identity provider factory for that provider id
        
        Args:
            realm (str):  [required]
            provider_id (str):  [required]
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/identity-provider/providers/{provider_id}
        """
        relative_url = f"{api_url}/{realm}/identity_provider/providers/{provider_id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()
