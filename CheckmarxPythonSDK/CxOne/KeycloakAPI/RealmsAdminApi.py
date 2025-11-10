from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.AdminEventRepresentation import AdminEventRepresentation
from .dto.ClientPoliciesRepresentation import ClientPoliciesRepresentation
from .dto.ClientProfilesRepresentation import ClientProfilesRepresentation
from .dto.ClientRepresentation import ClientRepresentation
from .dto.ClientScopeRepresentation import ClientScopeRepresentation
from .dto.EventRepresentation import EventRepresentation
from .dto.GlobalRequestResult import GlobalRequestResult
from .dto.GroupRepresentation import GroupRepresentation
from .dto.ManagementPermissionReference import ManagementPermissionReference
from .dto.RealmEventsConfigRepresentation import RealmEventsConfigRepresentation
from .dto.RealmRepresentation import RealmRepresentation
from .api_url import api_url


class RealmsAdminApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get(self, brief_representation: str = None) -> List[RealmRepresentation]:
        """
        Get accessible realms Returns a list of accessible realms. The list is filtered based on what realms the caller is allowed to view.
        
        Args:
            brief_representation (str): 
        
        Returns:
            List[RealmRepresentation]
        
        URL:
            Relative path: /
        """
        params = {"briefRepresentation": brief_representation}
        relative_url = f"{api_url}/"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [RealmRepresentation.from_dict(item) for item in response.json()]

    def post(self, ) -> bool:
        """
        Import a realm. Imports a realm from a full representation of that realm.
        
        Returns:
            bool
        
        URL:
            Relative path: /
        """
        relative_url = f"{api_url}/"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def get_by_realm(self, realm: str) -> RealmRepresentation:
        """
        Get the top-level representation of the realm It will not include nested information like User and Client representations.
        
        Args:
            realm (str):  [required]
        
        Returns:
            RealmRepresentation
        
        URL:
            Relative path: /{realm}
        """
        relative_url = f"{api_url}/{realm}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return RealmRepresentation.from_dict(response.json())

    def put_by_realm(self, realm: str, realm_representation: RealmRepresentation) -> bool:
        """
        Update the top-level information of the realm Any user, roles or client information in the representation will be ignored.
        
        Args:
            realm (str):  [required]
            realm_representation (RealmRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}
        """
        relative_url = f"{api_url}/{realm}"
        response = self.api_client.put_request(relative_url=relative_url, json=realm_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

    def delete_by_realm(self, realm: str) -> bool:
        """
        Delete the realm
        
        Args:
            realm (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}
        """
        relative_url = f"{api_url}/{realm}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_admin_events(self, realm: str, auth_client: str = None, auth_ip_address: str = None, auth_realm: str = None,
                         auth_user: str = None, date_from: str = None, date_to: str = None, first: str = None,
                         max: str = None, operation_types: str = None, resource_path: str = None,
                         resource_types: str = None) -> List[AdminEventRepresentation]:
        """
        Get admin events Returns all admin events, or filters events based on URL query parameters listed here
        
        Args:
            realm (str):  [required]
            auth_client (str): 
            auth_ip_address (str): 
            auth_realm (str): 
            auth_user (str): user id
            date_from (str): 
            date_to (str): 
            first (str): 
            max (str): Maximum results size (defaults to 100)
            operation_types (str): [String]
            resource_path (str): 
            resource_types (str): [String]
        
        Returns:
            List[AdminEventRepresentation]
        
        URL:
            Relative path: /{realm}/admin-events
        """
        params = {"authClient": auth_client, "authIpAddress": auth_ip_address, "authRealm": auth_realm,
                  "authUser": auth_user, "dateFrom": date_from, "dateTo": date_to, "first": first, "max": max,
                  "operationTypes": operation_types, "resourcePath": resource_path, "resourceTypes": resource_types}
        relative_url = f"{api_url}/{realm}/admin_events"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [AdminEventRepresentation.from_dict(item) for item in response.json()]

    def delete_admin_events(self, realm: str) -> bool:
        """
        Delete all admin events
        
        Args:
            realm (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/admin-events
        """
        relative_url = f"{api_url}/{realm}/admin_events"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_client_description_converter(self, realm: str) -> ClientRepresentation:
        """
        Base path for importing clients under this realm.
        
        Args:
            realm (str):  [required]
        
        Returns:
            ClientRepresentation
        
        URL:
            Relative path: /{realm}/client-description-converter
        """
        relative_url = f"{api_url}/{realm}/client_description_converter"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return ClientRepresentation.from_dict(response.json())

    def get_policies(self, realm: str) -> ClientPoliciesRepresentation:
        """
        
        Args:
            realm (str):  [required]
        
        Returns:
            ClientPoliciesRepresentation
        
        URL:
            Relative path: /{realm}/client-policies/policies
        """
        relative_url = f"{api_url}/{realm}/client_policies/policies"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ClientPoliciesRepresentation.from_dict(response.json())

    def put_policies(self, realm: str, client_policies_representation: ClientPoliciesRepresentation) -> bool:
        """
        
        Args:
            realm (str):  [required]
            client_policies_representation (ClientPoliciesRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-policies/policies
        """
        relative_url = f"{api_url}/{realm}/client_policies/policies"
        response = self.api_client.put_request(relative_url=relative_url, json=client_policies_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

    def get_profiles(self, realm: str, include_global_profiles: str = None) -> ClientProfilesRepresentation:
        """
        
        Args:
            realm (str):  [required]
            include_global_profiles (str): 
        
        Returns:
            ClientProfilesRepresentation
        
        URL:
            Relative path: /{realm}/client-policies/profiles
        """
        params = {"include-global-profiles": include_global_profiles}
        relative_url = f"{api_url}/{realm}/client_policies/profiles"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return ClientProfilesRepresentation.from_dict(response.json())

    def put_profiles(self, realm: str, client_profiles_representation: ClientProfilesRepresentation) -> bool:
        """
        
        Args:
            realm (str):  [required]
            client_profiles_representation (ClientProfilesRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/client-policies/profiles
        """
        relative_url = f"{api_url}/{realm}/client_policies/profiles"
        response = self.api_client.put_request(relative_url=relative_url, json=client_profiles_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

    def get_client_session_stats(self, realm: str) -> List[str]:
        """
        Get client session stats Returns a JSON map.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[str]
        
        URL:
            Relative path: /{realm}/client-session-stats
        """
        relative_url = f"{api_url}/{realm}/client_session_stats"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_credential_registrators(self, realm: str) -> List[str]:
        """
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[str]
        
        URL:
            Relative path: /{realm}/credential-registrators
        """
        relative_url = f"{api_url}/{realm}/credential_registrators"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_default_default_client_scopes(self, realm: str) -> List[ClientScopeRepresentation]:
        """
        Get realm default client scopes.  Only name and ids are returned.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[ClientScopeRepresentation]
        
        URL:
            Relative path: /{realm}/default-default-client-scopes
        """
        relative_url = f"{api_url}/{realm}/default_default_client_scopes"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ClientScopeRepresentation.from_dict(item) for item in response.json()]

    def put_default_default_client_scope(self, realm: str, client_scope_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            client_scope_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/default-default-client-scopes/{clientScopeId}
        """
        relative_url = f"{api_url}/{realm}/default_default_client_scopes/{client_scope_id}"
        response = self.api_client.put_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def delete_default_default_client_scope(self, realm: str, client_scope_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            client_scope_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/default-default-client-scopes/{clientScopeId}
        """
        relative_url = f"{api_url}/{realm}/default_default_client_scopes/{client_scope_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_default_groups(self, realm: str) -> List[GroupRepresentation]:
        """
        Get group hierarchy.  Only name and ids are returned.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[GroupRepresentation]
        
        URL:
            Relative path: /{realm}/default-groups
        """
        relative_url = f"{api_url}/{realm}/default_groups"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [GroupRepresentation.from_dict(item) for item in response.json()]

    def put_default_group(self, realm: str, group_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            group_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/default-groups/{groupId}
        """
        relative_url = f"{api_url}/{realm}/default_groups/{group_id}"
        response = self.api_client.put_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def delete_default_group(self, realm: str, group_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            group_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/default-groups/{groupId}
        """
        relative_url = f"{api_url}/{realm}/default_groups/{group_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_default_optional_client_scopes(self, realm: str) -> List[ClientScopeRepresentation]:
        """
        Get realm optional client scopes.  Only name and ids are returned.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[ClientScopeRepresentation]
        
        URL:
            Relative path: /{realm}/default-optional-client-scopes
        """
        relative_url = f"{api_url}/{realm}/default_optional_client_scopes"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ClientScopeRepresentation.from_dict(item) for item in response.json()]

    def put_default_optional_client_scope(self, realm: str, client_scope_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            client_scope_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/default-optional-client-scopes/{clientScopeId}
        """
        relative_url = f"{api_url}/{realm}/default_optional_client_scopes/{client_scope_id}"
        response = self.api_client.put_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def delete_default_optional_client_scope(self, realm: str, client_scope_id: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            client_scope_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/default-optional-client-scopes/{clientScopeId}
        """
        relative_url = f"{api_url}/{realm}/default_optional_client_scopes/{client_scope_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_events(self, realm: str, client: str = None, date_from: str = None, date_to: str = None, first: str = None,
                   ip_address: str = None, max: str = None, type: str = None, user: str = None) -> List[
        EventRepresentation]:
        """
        Get events Returns all events, or filters them based on URL query parameters listed here
        
        Args:
            realm (str):  [required]
            client (str): App or oauth client name
            date_from (str): From date
            date_to (str): To date
            first (str): Paging offset
            ip_address (str): IP Address
            max (str): Maximum results size (defaults to 100)
            type (str): The types of events to return [String]
            user (str): User id
        
        Returns:
            List[EventRepresentation]
        
        URL:
            Relative path: /{realm}/events
        """
        params = {"client": client, "dateFrom": date_from, "dateTo": date_to, "first": first, "ipAddress": ip_address,
                  "max": max, "type": type, "user": user}
        relative_url = f"{api_url}/{realm}/events"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [EventRepresentation.from_dict(item) for item in response.json()]

    def delete_events(self, realm: str) -> bool:
        """
        Delete all events
        
        Args:
            realm (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/events
        """
        relative_url = f"{api_url}/{realm}/events"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_events_config(self, realm: str) -> RealmEventsConfigRepresentation:
        """
        Get the events provider configuration Returns JSON object with events provider configuration
        
        Args:
            realm (str):  [required]
        
        Returns:
            RealmEventsConfigRepresentation
        
        URL:
            Relative path: /{realm}/events/config
        """
        relative_url = f"{api_url}/{realm}/events/config"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return RealmEventsConfigRepresentation.from_dict(response.json())

    def put_events_config(self, realm: str,
                          realm_events_config_representation: RealmEventsConfigRepresentation) -> bool:
        """
        
        Args:
            realm (str):  [required]
            realm_events_config_representation (RealmEventsConfigRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/events/config
        """
        relative_url = f"{api_url}/{realm}/events/config"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=realm_events_config_representation.to_dict(), is_iam=True)
        return response.status_code == 204

    def get_group_by_path(self, realm: str, path: str) -> GroupRepresentation:
        """
        
        Args:
            realm (str):  [required]
            path (str):  [required]
        
        Returns:
            GroupRepresentation
        
        URL:
            Relative path: /{realm}/group-by-path/{path}
        """
        relative_url = f"{api_url}/{realm}/group_by_path/{path}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return GroupRepresentation.from_dict(response.json())

    def get_localization_by_realm(self, realm: str) -> List[str]:
        """
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[str]
        
        URL:
            Relative path: /{realm}/localization
        """
        relative_url = f"{api_url}/{realm}/localization"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_localization_by_realm_by_locale(self, realm: str, locale: str,
                                            use_realm_default_locale_fallback: str = None) -> Dict[str, Any]:
        """
        
        Args:
            realm (str):  [required]
            locale (str):  [required]
            use_realm_default_locale_fallback (str): 
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/localization/{locale}
        """
        params = {"useRealmDefaultLocaleFallback": use_realm_default_locale_fallback}
        relative_url = f"{api_url}/{realm}/localization/{locale}"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return response.json()

    def post_localization(self, realm: str, locale: str) -> bool:
        """
        Import localization from uploaded JSON file
        
        Args:
            realm (str):  [required]
            locale (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/localization/{locale}
        """
        relative_url = f"{api_url}/{realm}/localization/{locale}"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 201

    def delete_localization_by_realm_by_locale(self, realm: str, locale: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            locale (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/localization/{locale}
        """
        relative_url = f"{api_url}/{realm}/localization/{locale}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_localization_by_realm_by_locale_by_key(self, realm: str, locale: str, key: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            locale (str):  [required]
            key (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/localization/{locale}/{key}
        """
        relative_url = f"{api_url}/{realm}/localization/{locale}/{key}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def put_localization(self, realm: str, locale: str, key: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            locale (str):  [required]
            key (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/localization/{locale}/{key}
        """
        relative_url = f"{api_url}/{realm}/localization/{locale}/{key}"
        response = self.api_client.put_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def delete_localization_by_realm_by_locale_by_key(self, realm: str, locale: str, key: str) -> bool:
        """
        
        Args:
            realm (str):  [required]
            locale (str):  [required]
            key (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/localization/{locale}/{key}
        """
        relative_url = f"{api_url}/{realm}/localization/{locale}/{key}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_logout_all(self, realm: str) -> GlobalRequestResult:
        """
        Removes all user sessions.
        
        Args:
            realm (str):  [required]
        
        Returns:
            GlobalRequestResult
        
        URL:
            Relative path: /{realm}/logout-all
        """
        relative_url = f"{api_url}/{realm}/logout_all"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return GlobalRequestResult.from_dict(response.json())

    def post_partial_export(self, realm: str, export_clients: str = None, export_groups_and_roles: str = None) -> bool:
        """
        Partial export of existing realm into a JSON file.
        
        Args:
            realm (str):  [required]
            export_clients (str): 
            export_groups_and_roles (str): 
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/partial-export
        """
        params = {"exportClients": export_clients, "exportGroupsAndRoles": export_groups_and_roles}
        relative_url = f"{api_url}/{realm}/partial_export"
        response = self.api_client.post_request(relative_url=relative_url, params=params, is_iam=True)
        return response.status_code == 200

    def post_partial_import(self, realm: str) -> bool:
        """
        Partial import from a JSON file to an existing realm.
        
        Args:
            realm (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/partialImport
        """
        relative_url = f"{api_url}/{realm}/partial_import"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def post_push_revocation_by_realm(self, realm: str) -> GlobalRequestResult:
        """
        Push the realm’s revocation policy to any client that has an admin url associated with it.
        
        Args:
            realm (str):  [required]
        
        Returns:
            GlobalRequestResult
        
        URL:
            Relative path: /{realm}/push-revocation
        """
        relative_url = f"{api_url}/{realm}/push_revocation"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return GlobalRequestResult.from_dict(response.json())

    def delete_session(self, realm: str, session: str) -> bool:
        """
        Remove a specific user session.
        
        Args:
            realm (str):  [required]
            session (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/sessions/{session}
        """
        relative_url = f"{api_url}/{realm}/sessions/{session}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_test_smtp_connection(self, realm: str) -> bool:
        """
        Test SMTP connection with current logged in user
        
        Args:
            realm (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/testSMTPConnection
        """
        relative_url = f"{api_url}/{realm}/test_smtp_connection"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def get_users_management_permissions(self, realm: str) -> ManagementPermissionReference:
        """
        
        Args:
            realm (str):  [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/users-management-permissions
        """
        relative_url = f"{api_url}/{realm}/users_management_permissions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())

    def put_users_management_permissions(self, realm: str,
                                         management_permission_reference: ManagementPermissionReference) -> ManagementPermissionReference:
        """
        
        Args:
            realm (str):  [required]
            management_permission_reference (ManagementPermissionReference): Request body data [required]
        
        Returns:
            ManagementPermissionReference
        
        URL:
            Relative path: /{realm}/users-management-permissions
        """
        relative_url = f"{api_url}/{realm}/users_management_permissions"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=management_permission_reference.to_dict(), is_iam=True)
        return ManagementPermissionReference.from_dict(response.json())
