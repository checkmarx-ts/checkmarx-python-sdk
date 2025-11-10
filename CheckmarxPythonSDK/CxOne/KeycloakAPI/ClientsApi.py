from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.AccessToken import AccessToken
from .dto.ClientRepresentation import ClientRepresentation
from .dto.ClientScopeRepresentation import ClientScopeRepresentation
from .dto.CredentialRepresentation import CredentialRepresentation
from .dto.GlobalRequestResult import GlobalRequestResult
from .dto.IDToken import IDToken
from .dto.ManagementPermissionReference import ManagementPermissionReference
from .dto.ProtocolMapperEvaluationRepresentation import ProtocolMapperEvaluationRepresentation
from .dto.RoleRepresentation import RoleRepresentation
from .dto.UserRepresentation import UserRepresentation
from .dto.UserSessionRepresentation import UserSessionRepresentation
from .api_url import api_url


class ClientsApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_clients(self, realm: str, client_id: str = None, first: str = None, max: str = None, q: str = None,
                    search: bool = None, viewable_only: str = None) -> List[ClientRepresentation]:
        """
        Get clients belonging to the realm.
        
        Args:
            realm (str):  [required]
            client_id (str): filter by clientId
            first (str): the first result
            max (str): the max results to return
            q (str): 
            search (bool): whether this is a search query or a getClientById query
            viewable_only (str): filter clients that cannot be viewed in full by admin
        
        Returns:
            List[ClientRepresentation]
        
        URL:
            Relative path: /{realm}/clients
        """
        params = {"clientId": client_id, "first": first, "max": max, "q": q, "search": search,
                  "viewableOnly": viewable_only}
        relative_url = f"{api_url}/{realm}/clients"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [ClientRepresentation.from_dict(item) for item in response.json()]

    def post_clients(self, realm: str, client_representation: ClientRepresentation) -> bool:
        """
        Create a new client Client’s client_id must be unique!
        
        Args:
            realm (str):  [required]
            client_representation (ClientRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients
        """
        relative_url = f"{api_url}/{realm}/clients"
        response = self.api_client.post_request(relative_url=relative_url, json=client_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 200

    def get_client_by_realm_by_id(self, realm: str, id: str) -> ClientRepresentation:
        """
        Get representation of the client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            ClientRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ClientRepresentation.from_dict(response.json())

    def put_client(self, realm: str, id: str, client_representation: ClientRepresentation) -> bool:
        """
        Update the client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_representation (ClientRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}"
        response = self.api_client.put_request(relative_url=relative_url, json=client_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

    def delete_client_by_realm_by_id(self, realm: str, id: str) -> bool:
        """
        Delete the client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_client_secret(self, realm: str, id: str) -> CredentialRepresentation:
        """
        Get the client secret
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            CredentialRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/client-secret
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/client_secret"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return CredentialRepresentation.from_dict(response.json())

    def post_client_secret(self, realm: str, id: str) -> CredentialRepresentation:
        """
        Generate a new secret for the client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            CredentialRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/client-secret
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/client_secret"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return CredentialRepresentation.from_dict(response.json())

    def get_rotated(self, realm: str, id: str) -> CredentialRepresentation:
        """
        Get the rotated client secret
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            CredentialRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/client-secret/rotated
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/client_secret/rotated"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return CredentialRepresentation.from_dict(response.json())

    def delete_rotated(self, realm: str, id: str) -> bool:
        """
        Invalidate the rotated secret for the client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/client-secret/rotated
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/client_secret/rotated"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def get_default_client_scopes(self, realm: str, id: str) -> List[ClientScopeRepresentation]:
        """
        Get default client scopes.  Only name and ids are returned.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[ClientScopeRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/default-client-scopes
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/default_client_scopes"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ClientScopeRepresentation.from_dict(item) for item in response.json()]

    def put_default_client_scope(self, realm: str, id: str, client_scope_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_scope_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/default-client-scopes/{clientScopeId}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/default_client_scopes/{client_scope_id}"
        response = self.api_client.put_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def delete_default_client_scope(self, realm: str, id: str, client_scope_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_scope_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/default-client-scopes/{clientScopeId}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/default_client_scopes/{client_scope_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_generate_example_access_token(self, realm: str, id: str, scope: str = None,
                                          user_id: str = None) -> AccessToken:
        """
        Create JSON with payload of example access token
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            scope (str): 
            user_id (str): 
        
        Returns:
            AccessToken
        
        URL:
            Relative path: /{realm}/clients/{id}/evaluate-scopes/generate-example-access-token
        """
        params = {"scope": scope, "userId": user_id}
        relative_url = f"{api_url}/{realm}/clients/{id}/evaluate_scopes/generate_example_access_token"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return AccessToken.from_dict(response.json())

    def get_generate_example_id_token(self, realm: str, id: str, scope: str = None, user_id: str = None) -> IDToken:
        """
        Create JSON with payload of example id token
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            scope (str): 
            user_id (str): 
        
        Returns:
            IDToken
        
        URL:
            Relative path: /{realm}/clients/{id}/evaluate-scopes/generate-example-id-token
        """
        params = {"scope": scope, "userId": user_id}
        relative_url = f"{api_url}/{realm}/clients/{id}/evaluate_scopes/generate_example_id_token"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return IDToken.from_dict(response.json())

    def get_generate_example_userinfo(self, realm: str, id: str, scope: str = None, user_id: str = None) -> Dict[
        str, Any]:
        """
        Create JSON with payload of example user info
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            scope (str): 
            user_id (str): 
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/clients/{id}/evaluate-scopes/generate-example-userinfo
        """
        params = {"scope": scope, "userId": user_id}
        relative_url = f"{api_url}/{realm}/clients/{id}/evaluate_scopes/generate_example_userinfo"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return response.json()

    def get_protocol_mappers(self, realm: str, id: str, scope: str = None) -> List[
        ProtocolMapperEvaluationRepresentation]:
        """
        Return list of all protocol mappers, which will be used when generating tokens issued for particular client.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            scope (str): 
        
        Returns:
            List[ProtocolMapperEvaluationRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/evaluate-scopes/protocol-mappers
        """
        params = {"scope": scope}
        relative_url = f"{api_url}/{realm}/clients/{id}/evaluate_scopes/protocol_mappers"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [ProtocolMapperEvaluationRepresentation.from_dict(item) for item in response.json()]

    def get_granted(self, realm: str, id: str, role_container_id: str, scope: str = None) -> List[RoleRepresentation]:
        """
        Get effective scope mapping of all roles of particular role container, which this client is defacto allowed to have in the accessToken issued for him.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_container_id (str):  [required]
            scope (str): 
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/evaluate-scopes/scope-mappings/{roleContainerId}/granted
        """
        params = {"scope": scope}
        relative_url = f"{api_url}/{realm}/clients/{id}/evaluate_scopes/scope_mappings/{role_container_id}/granted"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_not_granted(self, realm: str, id: str, role_container_id: str, scope: str = None) -> List[
        RoleRepresentation]:
        """
        Get roles, which this client doesn’t have scope for and can’t have them in the accessToken issued for him.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            role_container_id (str):  [required]
            scope (str): 
        
        Returns:
            List[RoleRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/evaluate-scopes/scope-mappings/{roleContainerId}/not-granted
        """
        params = {"scope": scope}
        relative_url = f"{api_url}/{realm}/clients/{id}/evaluate_scopes/scope_mappings/{role_container_id}/not_granted"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RoleRepresentation.from_dict(item) for item in response.json()]

    def get_installation_provider(self, realm: str, id: str, provider_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            provider_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/installation/providers/{providerId}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/installation/providers/{provider_id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def get_client_management_permissions(self, realm: str, id: str) -> ManagementPermissionReference:
        """
        Return object stating whether client Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/clients/{id}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/management/permissions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def put_client_management_permissions(self, realm: str, id: str,
                                          management_permission_reference: ManagementPermissionReference) -> ManagementPermissionReference:
        """
        Return object stating whether client Authorization permissions have been initialized or not and a reference
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            management_permission_reference (ManagementPermissionReference): Request body data [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/clients/{id}/management/permissions
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/management/permissions"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=management_permission_reference.to_dict(), is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def post_nodes(self, realm: str, id: str) -> bool:
        """
        Register a cluster node with the client Manually register cluster node to this client - usually it’s not needed to call this directly as adapter should handle by sending registration request to Keycloak
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/nodes
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/nodes"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 201

    def delete_node(self, realm: str, id: str, node: str) -> bool:
        """
        Unregister a cluster node from the client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            node (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/nodes/{node}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/nodes/{node}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_offline_session_count(self, realm: str, id: str) -> Dict[str, Any]:
        """
        Get application offline session count Returns a number of offline user sessions associated with this client { \"count\": number }
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/clients/{id}/offline-session-count
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/offline_session_count"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_offline_sessions(self, realm: str, id: str, first: str = None, max: str = None) -> List[
        UserSessionRepresentation]:
        """
        Get offline sessions for client Returns a list of offline user sessions associated with this client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            first (str): Paging offset
            max (str): Maximum results size (defaults to 100)
        
        Returns:
            List[UserSessionRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/offline-sessions
        """
        params = {"first": first, "max": max}
        relative_url = f"{api_url}/{realm}/clients/{id}/offline_sessions"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [UserSessionRepresentation.from_dict(item) for item in response.json()]

    def get_optional_client_scopes(self, realm: str, id: str) -> List[ClientScopeRepresentation]:
        """
        Get optional client scopes.  Only name and ids are returned.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[ClientScopeRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/optional-client-scopes
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/optional_client_scopes"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ClientScopeRepresentation.from_dict(item) for item in response.json()]

    def put_optional_client_scope(self, realm: str, id: str, client_scope_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_scope_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/optional-client-scopes/{clientScopeId}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/optional_client_scopes/{client_scope_id}"
        response = self.api_client.put_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def delete_optional_client_scope(self, realm: str, id: str, client_scope_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_scope_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/optional-client-scopes/{clientScopeId}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/optional_client_scopes/{client_scope_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_client_push_revocation(self, realm: str, id: str) -> GlobalRequestResult:
        """
        Push the client’s revocation policy to its admin URL If the client has an admin URL, push revocation policy to it.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            GlobalRequestResult
        
        URL:
            Relative path: /{realm}/clients/{id}/push-revocation
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/push_revocation"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return GlobalRequestResult.from_dict(response.json())

    def post_registration_access_token(self, realm: str, id: str) -> ClientRepresentation:
        """
        Generate a new registration access token for the client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            ClientRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/registration-access-token
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/registration_access_token"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return ClientRepresentation.from_dict(response.json())

    def get_service_account_user(self, realm: str, id: str) -> UserRepresentation:
        """
        Get a user dedicated to the service account
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            UserRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/service-account-user
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/service_account_user"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return UserRepresentation.from_dict(response.json())

    def get_session_count(self, realm: str, id: str) -> Dict[str, Any]:
        """
        Get application session count Returns a number of user sessions associated with this client { \"count\": number }
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/clients/{id}/session-count
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/session_count"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_test_nodes_available(self, realm: str, id: str) -> GlobalRequestResult:
        """
        Test if registered cluster nodes are available Tests availability by sending 'ping' request to all cluster nodes.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            GlobalRequestResult
        
        URL:
            Relative path: /{realm}/clients/{id}/test-nodes-available
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/test_nodes_available"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return GlobalRequestResult.from_dict(response.json())

    def get_client_user_sessions(self, realm: str, id: str, first: str = None, max: str = None) -> List[
        UserSessionRepresentation]:
        """
        Get user sessions for client Returns a list of user sessions associated with this client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            first (str): Paging offset
            max (str): Maximum results size (defaults to 100)
        
        Returns:
            List[UserSessionRepresentation]
        
        URL:
            Relative path: /{realm}/clients/{id}/user-sessions
        """
        params = {"first": first, "max": max}
        relative_url = f"{api_url}/{realm}/clients/{id}/user_sessions"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [UserSessionRepresentation.from_dict(item) for item in response.json()]
