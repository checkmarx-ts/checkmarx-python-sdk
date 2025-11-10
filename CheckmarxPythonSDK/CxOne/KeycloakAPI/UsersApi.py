from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.CredentialRepresentation import CredentialRepresentation
from .dto.FederatedIdentityRepresentation import FederatedIdentityRepresentation
from .dto.GroupRepresentation import GroupRepresentation
from .dto.UPConfig import UPConfig
from .dto.UserProfileMetadata import UserProfileMetadata
from .dto.UserRepresentation import UserRepresentation
from .dto.UserSessionRepresentation import UserSessionRepresentation
from .api_url import api_url


class UsersApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_users_by_realm(self, realm: str, brief_representation: bool = None, email: bool = None,
                           email_verified: bool = None, enabled: bool = None, exact: bool = None, first: str = None,
                           first_name: bool = None, idp_alias: str = None, idp_user_id: str = None,
                           last_name: bool = None, max: str = None, q: str = None, search: str = None,
                           username: str = None) -> List[UserRepresentation]:
        """
        Get users Returns a stream of users, filtered according to query parameters.
        
        Args:
            realm (str):  [required]
            brief_representation (bool): Boolean which defines whether brief representations are returned (default: false)
            email (bool): A String contained in email, or the complete email, if param "exact" is true
            email_verified (bool): whether the email has been verified
            enabled (bool): Boolean representing if user is enabled or not
            exact (bool): Boolean which defines whether the params "last", "first", "email" and "username" must match exactly
            first (str): Pagination offset
            first_name (bool): A String contained in firstName, or the complete firstName, if param "exact" is true
            idp_alias (str): The alias of an Identity Provider linked to the user
            idp_user_id (str): The userId at an Identity Provider linked to the user
            last_name (bool): A String contained in lastName, or the complete lastName, if param "exact" is true
            max (str): Maximum results size (defaults to 100)
            q (str): A query to search for custom attributes, in the format 'key1:value2 key2:value2'
            search (str): A String contained in username, first or last name, or email. Default search behavior is prefix-based (e.g., foo or foo*). Use foo for infix search and "foo" for exact search.
            username (str): A String contained in username, or the complete username, if param "exact" is true
        
        Returns:
            List[UserRepresentation]
        
        URL:
            Relative path: /{realm}/users
        """
        params = {"briefRepresentation": brief_representation, "email": email, "emailVerified": email_verified,
                  "enabled": enabled, "exact": exact, "first": first, "firstName": first_name, "idpAlias": idp_alias,
                  "idpUserId": idp_user_id, "lastName": last_name, "max": max, "q": q, "search": search,
                  "username": username}
        relative_url = f"{api_url}/{realm}/users"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [UserRepresentation.from_dict(item) for item in response.json()]

    def create_a_new_user(self, realm: str, user_representation: UserRepresentation) -> bool:
        """
        Create a new user Username must be unique.
        
        Args:
            realm (str):  [required]
            user_representation (UserRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users
        """
        relative_url = f"{api_url}/{realm}/users"
        response = self.api_client.post_request(relative_url=relative_url, json=user_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 200

    def get_users_count(self, realm: str, email: str = None, email_verified: str = None, enabled: bool = None,
                        first_name: str = None, last_name: str = None, q: str = None, search: str = None,
                        username: str = None) -> int:
        """
        Returns the number of users that match the given criteria.
        
        Args:
            realm (str):  [required]
            email (str): email filter
            email_verified (str): 
            enabled (bool): Boolean representing if user is enabled or not
            first_name (str): first name filter
            last_name (str): last name filter
            q (str): 
            search (str): arbitrary search string for all the fields below. Default search behavior is prefix-based (e.g., foo or foo*). Use foo for infix search and "foo" for exact search.
            username (str): username filter
        
        Returns:
            int
        
        URL:
            Relative path: /{realm}/users/count
        """
        params = {"email": email, "emailVerified": email_verified, "enabled": enabled, "firstName": first_name,
                  "lastName": last_name, "q": q, "search": search, "username": username}
        relative_url = f"{api_url}/{realm}/users/count"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return response.json()

    def get_profile(self, realm: str) -> UPConfig:
        """
        
        Args:
            realm (str):  [required]
        
        Returns:
            UPConfig
        
        URL:
            Relative path: /{realm}/users/profile
        """
        relative_url = f"{api_url}/{realm}/users/profile"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return UPConfig.from_dict(response.json())

    def put_profile(self, realm: str, up_config: UPConfig) -> UPConfig:
        """
        
        Args:
            realm (str):  [required]
            up_config (UPConfig): Request body data [required]
        
        Returns:
            UPConfig
        
        URL:
            Relative path: /{realm}/users/profile
        """
        relative_url = f"{api_url}/{realm}/users/profile"
        response = self.api_client.put_request(relative_url=relative_url, json=up_config.to_dict(), is_iam=True)
        return UPConfig.from_dict(response.json())

    def get_metadata(self, realm: str) -> UserProfileMetadata:
        """
        
        Args:
            realm (str):  [required]
        
        Returns:
            UserProfileMetadata
        
        URL:
            Relative path: /{realm}/users/profile/metadata
        """
        relative_url = f"{api_url}/{realm}/users/profile/metadata"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return UserProfileMetadata.from_dict(response.json())

    def get_user_by_realm_by_id(self, realm: str, id: str, user_profile_metadata: bool = None) -> UserRepresentation:
        """
        Get representation of the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            user_profile_metadata (bool): Indicates if the user profile metadata should be added to the response
        
        Returns:
            UserRepresentation
        
        URL:
            Relative path: /{realm}/users/{id}
        """
        params = {"userProfileMetadata": user_profile_metadata}
        relative_url = f"{api_url}/{realm}/users/{id}"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return UserRepresentation.from_dict(response.json())

    def put_user(self, realm: str, id: str, user_representation: UserRepresentation) -> bool:
        """
        Update the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            user_representation (UserRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}
        """
        relative_url = f"{api_url}/{realm}/users/{id}"
        response = self.api_client.put_request(relative_url=relative_url, json=user_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

    def delete_user_by_realm_by_id(self, realm: str, id: str) -> bool:
        """
        Delete the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}
        """
        relative_url = f"{api_url}/{realm}/users/{id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def get_configured_user_storage_credential_types(self, realm: str, id: str) -> List[str]:
        """
        Return credential types, which are provided by the user storage where user is stored.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[str]
        
        URL:
            Relative path: /{realm}/users/{id}/configured-user-storage-credential-types
        """
        relative_url = f"{api_url}/{realm}/users/{id}/configured_user_storage_credential_types"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_consents(self, realm: str, id: str) -> List[Dict[str, Any]]:
        """
        Get consents granted by the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[Dict[str, Any]]
        
        URL:
            Relative path: /{realm}/users/{id}/consents
        """
        relative_url = f"{api_url}/{realm}/users/{id}/consents"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def delete_consent(self, realm: str, id: str, client: str) -> bool:
        """
        Revoke consent and offline tokens for particular client from user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/consents/{client}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/consents/{client}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_credentials(self, realm: str, id: str) -> List[CredentialRepresentation]:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[CredentialRepresentation]
        
        URL:
            Relative path: /{realm}/users/{id}/credentials
        """
        relative_url = f"{api_url}/{realm}/users/{id}/credentials"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [CredentialRepresentation.from_dict(item) for item in response.json()]

    def delete_credential(self, realm: str, id: str, credential_id: str) -> bool:
        """
        Remove a credential for a user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            credential_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/credentials/{credentialId}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/credentials/{credential_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_move_after(self, realm: str, id: str, credential_id: str, new_previous_credential_id: str) -> bool:
        """
        Move a credential to a position behind another credential
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            credential_id (str):  [required]
            new_previous_credential_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/credentials/{credentialId}/moveAfter/{newPreviousCredentialId}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/credentials/{credential_id}/move_after/{new_previous_credential_id}"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 201

    def post_move_to_first(self, realm: str, id: str, credential_id: str) -> bool:
        """
        Move a credential to a first position in the credentials list of the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            credential_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/credentials/{credentialId}/moveToFirst
        """
        relative_url = f"{api_url}/{realm}/users/{id}/credentials/{credential_id}/move_to_first"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 201

    def put_user_label(self, realm: str, id: str, credential_id: str) -> bool:
        """
        Update a credential label for a user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            credential_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/credentials/{credentialId}/userLabel
        """
        relative_url = f"{api_url}/{realm}/users/{id}/credentials/{credential_id}/user_label"
        response = self.api_client.put_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def put_disable_credential_types(self, realm: str, id: str) -> bool:
        """
        Disable all credentials for a user of a specific type
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/disable-credential-types
        """
        relative_url = f"{api_url}/{realm}/users/{id}/disable_credential_types"
        response = self.api_client.put_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def put_execute_actions_email(self, realm: str, id: str, client_id: str = None, lifespan: str = None,
                                  redirect_uri: str = None) -> bool:
        """
        Send an email to the user with a link they can click to execute particular actions.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_id (str): Client id
            lifespan (str): Number of seconds after which the generated token expires
            redirect_uri (str): Redirect uri
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/execute-actions-email
        """
        params = {"client_id": client_id, "lifespan": lifespan, "redirect_uri": redirect_uri}
        relative_url = f"{api_url}/{realm}/users/{id}/execute_actions_email"
        response = self.api_client.put_request(relative_url=relative_url, params=params, is_iam=True)
        return response.status_code == 200

    def get_federated_identity(self, realm: str, id: str) -> List[FederatedIdentityRepresentation]:
        """
        Get social logins associated with the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[FederatedIdentityRepresentation]
        
        URL:
            Relative path: /{realm}/users/{id}/federated-identity
        """
        relative_url = f"{api_url}/{realm}/users/{id}/federated_identity"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [FederatedIdentityRepresentation.from_dict(item) for item in response.json()]

    def post_federated_identity(self, realm: str, id: str, provider: str) -> bool:
        """
        Add a social login provider to the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            provider (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/federated-identity/{provider}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/federated_identity/{provider}"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def delete_federated_identity(self, realm: str, id: str, provider: str) -> bool:
        """
        Remove a social login provider from user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            provider (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/federated-identity/{provider}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/federated_identity/{provider}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_user_groups(self, realm: str, id: str, brief_representation: str = None, first: str = None, max: str = None,
                        search: str = None) -> List[GroupRepresentation]:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            brief_representation (str): 
            first (str): 
            max (str): 
            search (str): 
        
        Returns:
            List[GroupRepresentation]
        
        URL:
            Relative path: /{realm}/users/{id}/groups
        """
        params = {"briefRepresentation": brief_representation, "first": first, "max": max, "search": search}
        relative_url = f"{api_url}/{realm}/users/{id}/groups"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [GroupRepresentation.from_dict(item) for item in response.json()]

    def get_user_groups_count(self, realm: str, id: str, search: str = None) -> Dict[str, Any]:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            search (str): 
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/users/{id}/groups/count
        """
        params = {"search": search}
        relative_url = f"{api_url}/{realm}/users/{id}/groups/count"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return response.json()

    def put_user_group(self, realm: str, id: str, group_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            group_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/groups/{groupId}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/groups/{group_id}"
        response = self.api_client.put_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def delete_user_group(self, realm: str, id: str, group_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            group_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/groups/{groupId}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/groups/{group_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_impersonation(self, realm: str, id: str) -> Dict[str, Any]:
        """
        Impersonate the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/users/{id}/impersonation
        """
        relative_url = f"{api_url}/{realm}/users/{id}/impersonation"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def post_logout(self, realm: str, id: str) -> bool:
        """
        Remove all user sessions associated with the user Also send notification to all clients that have an admin URL to invalidate the sessions for the particular user.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/logout
        """
        relative_url = f"{api_url}/{realm}/users/{id}/logout"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 201

    def get_offline_session(self, realm: str, id: str, client_uuid: str) -> List[UserSessionRepresentation]:
        """
        Get offline sessions associated with the user and client
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_uuid (str):  [required]
        
        Returns:
            List[UserSessionRepresentation]
        
        URL:
            Relative path: /{realm}/users/{id}/offline-sessions/{clientUuid}
        """
        relative_url = f"{api_url}/{realm}/users/{id}/offline_sessions/{client_uuid}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [UserSessionRepresentation.from_dict(item) for item in response.json()]

    def put_reset_password(self, realm: str, id: str, credential_representation: CredentialRepresentation) -> bool:
        """
        Set up a new password for the user.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            credential_representation (CredentialRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/reset-password
        """
        relative_url = f"{api_url}/{realm}/users/{id}/reset_password"
        response = self.api_client.put_request(relative_url=relative_url, json=credential_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 204

    def put_reset_password_email(self, realm: str, id: str, client_id: str = None, redirect_uri: str = None) -> bool:
        """
        Send an email to the user with a link they can click to reset their password.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_id (str): client id
            redirect_uri (str): redirect uri
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/reset-password-email
        """
        params = {"client_id": client_id, "redirect_uri": redirect_uri}
        relative_url = f"{api_url}/{realm}/users/{id}/reset_password_email"
        response = self.api_client.put_request(relative_url=relative_url, params=params, is_iam=True)
        return response.status_code == 200

    def put_send_verify_email(self, realm: str, id: str, client_id: str = None, redirect_uri: str = None) -> bool:
        """
        Send an email-verification email to the user An email contains a link the user can click to verify their email address.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            client_id (str): Client id
            redirect_uri (str): Redirect uri
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/users/{id}/send-verify-email
        """
        params = {"client_id": client_id, "redirect_uri": redirect_uri}
        relative_url = f"{api_url}/{realm}/users/{id}/send_verify_email"
        response = self.api_client.put_request(relative_url=relative_url, params=params, is_iam=True)
        return response.status_code == 200

    def get_sessions(self, realm: str, id: str) -> List[UserSessionRepresentation]:
        """
        Get sessions associated with the user
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            List[UserSessionRepresentation]
        
        URL:
            Relative path: /{realm}/users/{id}/sessions
        """
        relative_url = f"{api_url}/{realm}/users/{id}/sessions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [UserSessionRepresentation.from_dict(item) for item in response.json()]
