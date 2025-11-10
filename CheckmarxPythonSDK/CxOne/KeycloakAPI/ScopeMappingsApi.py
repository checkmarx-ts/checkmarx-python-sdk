from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.MappingsRepresentation import MappingsRepresentation
from .dto.RoleRepresentation import RoleRepresentation
from .api_url import api_url


class ScopeMappingsApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_client_scope_scope_mappings(self, realm: str, id: str) -> MappingsRepresentation:
        """
        Get all scope mappings for the client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            MappingsRepresentation
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return MappingsRepresentation.from_dict(response.json())

    def get_client_scope_scope_mappings_client(self, realm: str, id: str, client: str) -> List[RoleRepresentation]:
        """
        Get the roles associated with a client’s scope Returns roles for the client.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings/clients/{client}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_client_scope_scope_mappings_client(self, realm: str, id: str, client: str,
                                                role_representation: RoleRepresentation) -> bool:
        """
        Add client-level roles to the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings/clients/{client}"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_client_scope_scope_mappings_client(self, realm: str, id: str, client: str) -> bool:
        """
        Remove client-level roles from the client’s scope.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings/clients/{client}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_client_scope_scope_mappings_client_available(self, realm: str, id: str, client: str) -> List[
        RoleRepresentation]:
        """
        The available client-level roles Returns the roles for the client that can be associated with the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings/clients/{client}/available
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings/clients/{client}/available"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_scope_scope_mappings_client_composite(self, realm: str, id: str, client: str,
                                                         brief_representation: bool = None) -> List[RoleRepresentation]:
        """
        Get effective client roles Returns the roles for the client that are associated with the client’s scope.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
            brief_representation (bool): if false, return roles with their attributes
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings/clients/{client}/composite
        """
        params = {"briefRepresentation": brief_representation}
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings/clients/{client}/composite"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_scope_scope_mappings_realm(self, realm: str, id: str) -> List[RoleRepresentation]:
        """
        Get realm-level roles associated with the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings/realm
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings/realm"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_client_scope_scope_mappings_realm(self, realm: str, id: str,
                                               role_representation: RoleRepresentation) -> bool:
        """
        Add a set of realm-level roles to the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings/realm
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings/realm"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_client_scope_scope_mappings_realm(self, realm: str, id: str) -> bool:
        """
        Remove a set of realm-level roles from the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings/realm
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings/realm"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_client_scope_scope_mappings_realm_available(self, realm: str, id: str) -> List[RoleRepresentation]:
        """
        Get realm-level roles that are available to attach to this client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings/realm/available
        """
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings/realm/available"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_scope_scope_mappings_realm_composite(self, realm: str, id: str, brief_representation: bool = None) -> \
    List[RoleRepresentation]:
        """
        Get effective realm-level roles associated with the client’s scope What this does is recurse any composite roles associated with the client’s scope and adds the roles to this lists.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            brief_representation (bool): if false, return roles with their attributes
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-scopes/{id}/scope-mappings/realm/composite
        """
        params = {"briefRepresentation": brief_representation}
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/scope_mappings/realm/composite"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_template_scope_mappings(self, realm: str, id: str) -> MappingsRepresentation:
        """
        Get all scope mappings for the client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            MappingsRepresentation
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return MappingsRepresentation.from_dict(response.json())

    def get_client_template_scope_mappings_client(self, realm: str, id: str, client: str) -> List[RoleRepresentation]:
        """
        Get the roles associated with a client’s scope Returns roles for the client.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings/clients/{client}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_client_template_scope_mappings_client(self, realm: str, id: str, client: str,
                                                   role_representation: RoleRepresentation) -> bool:
        """
        Add client-level roles to the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings/clients/{client}"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_client_template_scope_mappings_client(self, realm: str, id: str, client: str) -> bool:
        """
        Remove client-level roles from the client’s scope.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings/clients/{client}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_client_template_scope_mappings_client_available(self, realm: str, id: str, client: str) -> List[
        RoleRepresentation]:
        """
        The available client-level roles Returns the roles for the client that can be associated with the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings/clients/{client}/available
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings/clients/{client}/available"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_template_scope_mappings_client_composite(self, realm: str, id: str, client: str,
                                                            brief_representation: bool = None) -> List[
        RoleRepresentation]:
        """
        Get effective client roles Returns the roles for the client that are associated with the client’s scope.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
            brief_representation (bool): if false, return roles with their attributes
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings/clients/{client}/composite
        """
        params = {"briefRepresentation": brief_representation}
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings/clients/{client}/composite"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_template_scope_mappings_realm(self, realm: str, id: str) -> List[RoleRepresentation]:
        """
        Get realm-level roles associated with the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings/realm
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings/realm"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_client_template_scope_mappings_realm(self, realm: str, id: str,
                                                  role_representation: RoleRepresentation) -> bool:
        """
        Add a set of realm-level roles to the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings/realm
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings/realm"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_client_template_scope_mappings_realm(self, realm: str, id: str) -> bool:
        """
        Remove a set of realm-level roles from the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings/realm
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings/realm"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_client_template_scope_mappings_realm_available(self, realm: str, id: str) -> List[RoleRepresentation]:
        """
        Get realm-level roles that are available to attach to this client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings/realm/available
        """
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings/realm/available"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_template_scope_mappings_realm_composite(self, realm: str, id: str,
                                                           brief_representation: bool = None) -> List[
        RoleRepresentation]:
        """
        Get effective realm-level roles associated with the client’s scope What this does is recurse any composite roles associated with the client’s scope and adds the roles to this lists.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            brief_representation (bool): if false, return roles with their attributes
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/client-templates/{id}/scope-mappings/realm/composite
        """
        params = {"briefRepresentation": brief_representation}
        relative_url = f"{api_url}/{realm}/client_templates/{id}/scope_mappings/realm/composite"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_scope_mappings(self, realm: str, id: str) -> MappingsRepresentation:
        """
        Get all scope mappings for the client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            MappingsRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return MappingsRepresentation.from_dict(response.json())

    def get_client_scope_mappings_client(self, realm: str, id: str, client: str) -> List[RoleRepresentation]:
        """
        Get the roles associated with a client’s scope Returns roles for the client.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings/clients/{client}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_client_scope_mappings_client(self, realm: str, id: str, client: str,
                                          role_representation: RoleRepresentation) -> bool:
        """
        Add client-level roles to the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings/clients/{client}"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_client_scope_mappings_client(self, realm: str, id: str, client: str) -> bool:
        """
        Remove client-level roles from the client’s scope.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings/clients/{client}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings/clients/{client}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_client_scope_mappings_client_available(self, realm: str, id: str, client: str) -> List[RoleRepresentation]:
        """
        The available client-level roles Returns the roles for the client that can be associated with the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings/clients/{client}/available
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings/clients/{client}/available"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_scope_mappings_client_composite(self, realm: str, id: str, client: str,
                                                   brief_representation: bool = None) -> List[RoleRepresentation]:
        """
        Get effective client roles Returns the roles for the client that are associated with the client’s scope.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
            brief_representation (bool): if false, return roles with their attributes
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings/clients/{client}/composite
        """
        params = {"briefRepresentation": brief_representation}
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings/clients/{client}/composite"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_scope_mappings_realm(self, realm: str, id: str) -> List[RoleRepresentation]:
        """
        Get realm-level roles associated with the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings/realm
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings/realm"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def post_client_scope_mappings_realm(self, realm: str, id: str, role_representation: RoleRepresentation) -> bool:
        """
        Add a set of realm-level roles to the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_representation (RoleRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings/realm
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings/realm"
        response = self.api_client.post_request(relative_url=relative_url, json=role_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 201

    def delete_client_scope_mappings_realm(self, realm: str, id: str) -> bool:
        """
        Remove a set of realm-level roles from the client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings/realm
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings/realm"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_client_scope_mappings_realm_available(self, realm: str, id: str) -> List[RoleRepresentation]:
        """
        Get realm-level roles that are available to attach to this client’s scope
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings/realm/available
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings/realm/available"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_client_scope_mappings_realm_composite(self, realm: str, id: str, brief_representation: bool = None) -> List[
        RoleRepresentation]:
        """
        Get effective realm-level roles associated with the client’s scope What this does is recurse any composite roles associated with the client’s scope and adds the roles to this lists.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            brief_representation (bool): if false, return roles with their attributes
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/scope-mappings/realm/composite
        """
        params = {"briefRepresentation": brief_representation}
        relative_url = f"{api_url}/{realm}/clients/{id}/scope_mappings/realm/composite"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]
