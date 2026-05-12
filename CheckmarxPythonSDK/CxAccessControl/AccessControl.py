from dataclasses import asdict
import json
import os
from typing import List, Union

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT, CREATED
from .accesscontrol.dto import (
    AuthenticationProvider,
    LDAPGroup,
    LDAPRoleMapping,
    LDAPServer,
    LDAPTeamMapping,
    MyProfile,
    OIDCClient,
    Permission,
    Role,
    SAMLIdentityProvider,
    SAMLRoleMapping,
    SAMLServiceProvider,
    SAMLTeamMapping,
    ServiceProvider,
    SMTPSetting,
    SystemLocale,
    Team,
    User,
    WindowsDomain,
)
from .accesscontrol.dto.requests import (
    FirstAdminUserRequest,
    LDAPRoleMappingRequest,
    LDAPServerRequest,
    LDAPTeamMappingRequest,
    MyProfileUpdateRequest,
    OIDCClientRequest,
    RoleRequest,
    SMTPSettingRequest,
    UserRequest,
)


class AccessControl:

    def __init__(self, api_client: ApiClient = None, ac_url: str = None):
        self.api_client = api_client
        if ac_url is None:
            self.ac_url = f"{api_client.configuration.server_base_url.rstrip('/')}/cxrestapi/auth"
        else:
            self.ac_url = ac_url

    def get_all_assignable_users(self) -> List[User]:
        url = self.ac_url + "/AssignableUsers"
        response = self.api_client.call_api("GET", url)
        return [User.from_dict(item) for item in response.json() or []]

    def get_all_authentication_providers(self) -> List[AuthenticationProvider]:
        url = self.ac_url + "/AuthenticationProviders"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [AuthenticationProvider.from_dict(item) for item in response.json()]
        return []

    def submit_first_admin_user(
        self, username: str, password: str, first_name: str, last_name: str, email: str
    ) -> bool:
        req = FirstAdminUserRequest(
            username=username,
            password=password,
            firstName=first_name,
            lastName=last_name,
            email=email,
        )
        url = self.ac_url + "/Users/FirstAdmin"
        response = self.api_client.call_api(
            "POST", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == CREATED

    def get_admin_user_exists_confirmation(self) -> bool:
        url = self.ac_url + "/Users/FirstAdminExistence"
        response = self.api_client.call_api("GET", url)
        return response.status_code == OK and bool(response.json().get("firstAdminExists"))

    def get_all_ldap_role_mapping(self, ldap_server_id: int = None) -> List[LDAPRoleMapping]:
        url = self.ac_url + "/LDAPRoleMappings"
        if ldap_server_id:
            url += "?ldapServerId={id}".format(id=ldap_server_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [LDAPRoleMapping.from_dict(item) for item in response.json()]
        return []

    def update_ldap_role_mapping(
        self,
        ldap_server_id: int,
        role_id: int,
        ldap_group_dn: str,
        ldap_group_display_name: str,
    ) -> bool:
        req = LDAPRoleMappingRequest(
            roleId=role_id,
            ldapGroupDn=ldap_group_dn,
            ldapGroupDisplayName=ldap_group_display_name,
        )
        url = self.ac_url + "/LDAPServers/{id}/RoleMappings".format(id=ldap_server_id)
        response = self.api_client.call_api(
            "PUT", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == NO_CONTENT

    def delete_ldap_role_mapping(self, ldap_role_mapping_id: int) -> bool:
        url = self.ac_url + "/LDAPRoleMappings/{id}".format(id=ldap_role_mapping_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def test_ldap_server_connection(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        use_ssl: bool,
        verify_ssl_certificate: bool,
        base_dn: str,
        user_object_filter: str,
        user_object_class: str,
        username_attribute: str,
        first_name_attribute: str,
        last_name_attribute: str,
        email_attribute: str,
        synchronization_enabled: bool,
        advanced_team_and_role_mapping_enabled: bool,
        additional_group_dn: str,
        group_object_class: str,
        group_object_filter: str,
        group_name_attribute: str,
        group_members_attribute: str,
        user_membership_attribute: str,
    ) -> bool:
        req = LDAPServerRequest(
            host=host,
            port=port,
            username=username,
            password=password,
            useSsl=use_ssl,
            verifySslCertificate=verify_ssl_certificate,
            baseDn=base_dn,
            userObjectFilter=user_object_filter,
            userObjectClass=user_object_class,
            usernameAttribute=username_attribute,
            firstNameAttribute=first_name_attribute,
            lastNameAttribute=last_name_attribute,
            emailAttribute=email_attribute,
            synchronizationEnabled=synchronization_enabled,
            advancedTeamAndRoleMappingEnabled=advanced_team_and_role_mapping_enabled,
            additionalGroupDn=additional_group_dn,
            groupObjectClass=group_object_class,
            groupObjectFilter=group_object_filter,
            groupNameAttribute=group_name_attribute,
            groupMembersAttribute=group_members_attribute,
            userMembershipAttribute=user_membership_attribute,
        )
        url = self.ac_url + "/LDAPServers/TestConnection"
        response = self.api_client.call_api(
            "POST", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == OK

    def get_user_entries_by_search_criteria(
        self, ldap_server_id: int, username_contains_pattern: str = None
    ) -> List[User]:
        url = self.ac_url + "/LDAPServers/{id}/UserEntries".format(id=ldap_server_id)
        if username_contains_pattern:
            url += "?userNameContainsPattern={}".format(username_contains_pattern)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [User.from_dict(item) for item in response.json()]
        return []

    def get_group_entries_by_search_criteria(
        self, ldap_server_id: int, name_contains_pattern: str
    ) -> List[LDAPGroup]:
        url = self.ac_url + "/LDAPServers/{id}/GroupEntries".format(id=ldap_server_id)
        if name_contains_pattern:
            url += "?nameContainsPattern={}".format(name_contains_pattern)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [LDAPGroup.from_dict(item) for item in response.json()]
        return []

    def get_all_ldap_servers(self) -> List[LDAPServer]:
        url = self.ac_url + "/LDAPServers"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [LDAPServer.from_dict(item) for item in response.json()]
        return []

    def create_new_ldap_server(
        self,
        password: str,
        active: bool,
        name: str,
        host: str,
        port: int,
        username: str,
        use_ssl: bool,
        verify_ssl_certificate: bool,
        based_dn: str,
        additional_user_dn: str,
        user_object_filter: str,
        user_object_class: str,
        username_attribute: str,
        first_name_attribute: str,
        last_name_attribute: str,
        email_attribute: str,
        ldap_directory_type: str,
        sso_enabled: bool,
        synchronization_enabled: bool,
        default_team_id: int,
        default_role_id: int,
        update_team_and_role_upon_login_enabled: bool,
        periodical_synchronization_enabled: bool,
        advanced_team_and_role_mapping_enabled: bool,
        additional_group_dn: str,
        group_object_class: str,
        group_object_filter: str,
        group_name_attribute: str,
        group_members_attribute: str,
        user_membership_attribute: str,
    ) -> bool:
        req = LDAPServerRequest(
            password=password,
            active=active,
            name=name,
            host=host,
            port=port,
            username=username,
            useSsl=use_ssl,
            verifySslCertificate=verify_ssl_certificate,
            baseDn=based_dn,
            additionalUserDn=additional_user_dn,
            userObjectFilter=user_object_filter,
            userObjectClass=user_object_class,
            usernameAttribute=username_attribute,
            firstNameAttribute=first_name_attribute,
            lastNameAttribute=last_name_attribute,
            emailAttribute=email_attribute,
            ldapDirectoryType=ldap_directory_type,
            ssoEnabled=sso_enabled,
            synchronizationEnabled=synchronization_enabled,
            defaultTeamId=default_team_id,
            defaultRoleId=default_role_id,
            updateTeamAndRoleUponLoginEnabled=update_team_and_role_upon_login_enabled,
            periodicalSynchronizationEnabled=periodical_synchronization_enabled,
            advancedTeamAndRoleMappingEnabled=advanced_team_and_role_mapping_enabled,
            additionalGroupDn=additional_group_dn,
            groupObjectClass=group_object_class,
            groupObjectFilter=group_object_filter,
            groupNameAttribute=group_name_attribute,
            groupMembersAttribute=group_members_attribute,
            userMembershipAttribute=user_membership_attribute,
        )
        url = self.ac_url + "/LDAPServers"
        response = self.api_client.call_api(
            "POST", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == CREATED

    def get_ldap_server_by_id(self, ldap_server_id: int) -> LDAPServer:
        url = self.ac_url + "/LDAPServers/{id}".format(id=ldap_server_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return LDAPServer.from_dict(response.json())
        return None

    def update_ldap_server(
        self,
        ldap_server_id: int,
        password: str,
        active: bool,
        name: str,
        host: str,
        port: int,
        username: str,
        use_ssl: bool,
        verify_ssl_certificate: bool,
        based_dn: str,
        additional_user_dn: str,
        user_object_filter: str,
        user_object_class: str,
        username_attribute: str,
        first_name_attribute: str,
        last_name_attribute: str,
        email_attribute: str,
        ldap_directory_type: str,
        sso_enabled: bool,
        synchronization_enabled: bool,
        default_team_id: str,
        default_role_id: str,
        update_team_and_role_upon_login_enabled: bool,
        periodical_synchronization_enabled: bool,
        advanced_team_and_role_mapping_enabled: bool,
        additional_group_dn: str,
        group_object_class: str,
        group_object_filter: str,
        group_name_attribute: str,
        group_members_attribute: str,
        user_membership_attribute: str,
    ) -> bool:
        req = LDAPServerRequest(
            password=password,
            active=active,
            name=name,
            host=host,
            port=port,
            username=username,
            useSsl=use_ssl,
            verifySslCertificate=verify_ssl_certificate,
            baseDn=based_dn,
            additionalUserDn=additional_user_dn,
            userObjectFilter=user_object_filter,
            userObjectClass=user_object_class,
            usernameAttribute=username_attribute,
            firstNameAttribute=first_name_attribute,
            lastNameAttribute=last_name_attribute,
            emailAttribute=email_attribute,
            ldapDirectoryType=ldap_directory_type,
            ssoEnabled=sso_enabled,
            synchronizationEnabled=synchronization_enabled,
            defaultTeamId=default_team_id,
            defaultRoleId=default_role_id,
            updateTeamAndRoleUponLoginEnabled=update_team_and_role_upon_login_enabled,
            periodicalSynchronizationEnabled=periodical_synchronization_enabled,
            advancedTeamAndRoleMappingEnabled=advanced_team_and_role_mapping_enabled,
            additionalGroupDn=additional_group_dn,
            groupObjectClass=group_object_class,
            groupObjectFilter=group_object_filter,
            groupNameAttribute=group_name_attribute,
            groupMembersAttribute=group_members_attribute,
            userMembershipAttribute=user_membership_attribute,
        )
        url = self.ac_url + "/LDAPServers/{id}".format(id=ldap_server_id)
        response = self.api_client.call_api(
            "PUT", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == NO_CONTENT

    def delete_ldap_server(self, ldap_server_id: int) -> bool:
        url = self.ac_url + "/LDAPServers/{id}".format(id=ldap_server_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def get_ldap_team_mapping(
        self, ldap_server_id: int = None, team_id: int = None
    ) -> List[LDAPTeamMapping]:
        url = self.ac_url + "/LDAPTeamMappings"
        optionals = []
        if ldap_server_id:
            optionals.append("ldapServerId={id}".format(id=ldap_server_id))
        if team_id:
            optionals.append("teamId={id}".format(id=team_id))
        if optionals:
            url += "?" + "&".join(optionals)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [LDAPTeamMapping.from_dict(item) for item in response.json()]
        return []

    def update_ldap_team_mapping(
        self,
        ldap_server_id: int,
        team_id: int,
        ldap_group_dn: str,
        ldap_group_display_name: str,
    ) -> bool:
        req = LDAPTeamMappingRequest(
            teamId=team_id,
            ldapGroupDn=ldap_group_dn,
            ldapGroupDisplayName=ldap_group_display_name,
        )
        url = self.ac_url + "/LDAPServers/{id}/TeamMappings".format(id=ldap_server_id)
        response = self.api_client.call_api(
            "PUT", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == NO_CONTENT

    def delete_ldap_team_mapping(self, ldap_team_mapping_id: int) -> bool:
        url = self.ac_url + "/LDAPTeamMappings/{id}".format(id=ldap_team_mapping_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def get_my_profile(self) -> MyProfile:
        url = self.ac_url + "/MyProfile"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return MyProfile.from_dict(response.json())
        return None

    def update_my_profile(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        cell_phone_number: str,
        job_title: str,
        other: str,
        country: str,
        locale_id: int,
    ) -> bool:
        req = MyProfileUpdateRequest(
            firstName=first_name,
            lastName=last_name,
            email=email,
            phoneNumber=phone_number,
            cellPhoneNumber=cell_phone_number,
            jobTitle=job_title,
            other=other,
            country=country,
            localeId=locale_id,
        )
        url = self.ac_url + "/MyProfile"
        response = self.api_client.call_api(
            "PUT", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == NO_CONTENT

    def get_all_oidc_clients(self) -> List[OIDCClient]:
        url = self.ac_url + "/OIDCClients"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [OIDCClient.from_dict(item) for item in response.json()]
        return []

    def create_new_oidc_client(
        self,
        update_access_token_claims_on_refresh: bool,
        access_token_type: int,
        include_jwt_id: bool,
        always_include_user_claims_in_id_token: bool,
        client_id: str,
        client_name: str,
        allow_offline_access: bool,
        client_secrets: List[str],
        allow_grant_types: List[str],
        allowed_scopes: List[str],
        enabled: bool,
        require_client_secret: bool,
        redirect_uris: List[str],
        post_logout_redirect_uris: List[str],
        front_channel_logout_uri: str,
        front_channel_logout_session_required: bool,
        back_channel_logout_uri: str,
        back_channel_logout_session_required: bool,
        identity_token_life_time: int,
        access_token_life_time: int,
        authorization_code_life_time: int,
        absolute_refresh_token_life_time: int,
        sliding_refresh_token_life_time: int,
        refresh_token_usage: int,
        refresh_token_expiration: int,
        allowed_cors_origins: List[str],
        allowed_access_tokens_via_browser: bool,
        claims: List[str],
        client_claims_prefix: str,
    ) -> bool:
        req = OIDCClientRequest(
            updateAccessTokenClaimsOnRefresh=update_access_token_claims_on_refresh,
            accessTokenType=access_token_type,
            includeJwtId=include_jwt_id,
            alwaysIncludeUserClaimsInIdToken=always_include_user_claims_in_id_token,
            clientId=client_id,
            clientName=client_name,
            allowOfflineAccess=allow_offline_access,
            clientSecrets=client_secrets,
            allowedGrantTypes=allow_grant_types,
            allowedScopes=allowed_scopes,
            enabled=enabled,
            requireClientSecret=require_client_secret,
            redirectUris=redirect_uris,
            postLogoutRedirectUris=post_logout_redirect_uris,
            frontChannelLogoutUri=front_channel_logout_uri,
            frontChannelLogoutSessionRequired=front_channel_logout_session_required,
            backChannelLogoutUri=back_channel_logout_uri,
            backChannelLogoutSessionRequired=back_channel_logout_session_required,
            identityTokenLifetime=identity_token_life_time,
            accessTokenLifetime=access_token_life_time,
            authorizationCodeLifetime=authorization_code_life_time,
            absoluteRefreshTokenLifetime=absolute_refresh_token_life_time,
            slidingRefreshTokenLifetime=sliding_refresh_token_life_time,
            refreshTokenUsage=refresh_token_usage,
            refreshTokenExpiration=refresh_token_expiration,
            allowedCorsOrigins=allowed_cors_origins,
            allowAccessTokensViaBrowser=allowed_access_tokens_via_browser,
            claims=claims,
            clientClaimsPrefix=client_claims_prefix,
        )
        url = self.ac_url + "/OIDCClients"
        response = self.api_client.call_api(
            "POST", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == CREATED

    def get_oidc_client_by_id(self, oidc_client_id: int) -> OIDCClient:
        url = self.ac_url + "/OIDCClients/{id}".format(id=oidc_client_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return OIDCClient.from_dict(response.json())
        return None

    def update_an_oidc_client(
        self,
        oidc_client_id: int,
        update_access_token_claims_on_refresh: bool,
        access_token_type: int,
        include_jwt_id: bool,
        always_include_user_claims_in_id_token: bool,
        client_id: str,
        client_name: str,
        allow_offline_access: bool,
        client_secrets: List[str],
        allow_grant_types: List[str],
        allowed_scopes: List[str],
        enabled: bool,
        require_client_secret: bool,
        redirect_uris: List[str],
        post_logout_redirect_uris: List[str],
        front_channel_logout_uri: str,
        front_channel_logout_session_required: bool,
        back_channel_logout_uri: str,
        back_channel_logout_session_required: bool,
        identity_token_life_time: int,
        access_token_life_time: int,
        authorization_code_life_time: int,
        absolute_refresh_token_life_time: int,
        sliding_refresh_token_life_time: int,
        refresh_token_usage: int,
        refresh_token_expiration: int,
        allowed_cors_origins: List[str],
        allowed_access_tokens_via_browser: bool,
        claims: List[str],
        client_claims_prefix: str,
    ) -> bool:
        req = OIDCClientRequest(
            updateAccessTokenClaimsOnRefresh=update_access_token_claims_on_refresh,
            accessTokenType=access_token_type,
            includeJwtId=include_jwt_id,
            alwaysIncludeUserClaimsInIdToken=always_include_user_claims_in_id_token,
            clientId=client_id,
            clientName=client_name,
            allowOfflineAccess=allow_offline_access,
            clientSecrets=client_secrets,
            allowedGrantTypes=allow_grant_types,
            allowedScopes=allowed_scopes,
            enabled=enabled,
            requireClientSecret=require_client_secret,
            redirectUris=redirect_uris,
            postLogoutRedirectUris=post_logout_redirect_uris,
            frontChannelLogoutUri=front_channel_logout_uri,
            frontChannelLogoutSessionRequired=front_channel_logout_session_required,
            backChannelLogoutUri=back_channel_logout_uri,
            backChannelLogoutSessionRequired=back_channel_logout_session_required,
            identityTokenLifetime=identity_token_life_time,
            accessTokenLifetime=access_token_life_time,
            authorizationCodeLifetime=authorization_code_life_time,
            absoluteRefreshTokenLifetime=absolute_refresh_token_life_time,
            slidingRefreshTokenLifetime=sliding_refresh_token_life_time,
            refreshTokenUsage=refresh_token_usage,
            refreshTokenExpiration=refresh_token_expiration,
            allowedCorsOrigins=allowed_cors_origins,
            allowAccessTokensViaBrowser=allowed_access_tokens_via_browser,
            claims=claims,
            clientClaimsPrefix=client_claims_prefix,
        )
        url = self.ac_url + "/OIDCClients/{id}".format(id=oidc_client_id)
        response = self.api_client.call_api(
            "PUT", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == NO_CONTENT

    def delete_an_oidc_client(self, oidc_client_id: int) -> bool:
        url = self.ac_url + "/OIDCClients/{id}".format(id=oidc_client_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def get_all_permissions(self) -> List[Permission]:
        url = self.ac_url + "/Permissions"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [Permission.from_dict(item) for item in response.json()]
        return []

    def get_permission_by_id(self, permission_id: int) -> Permission:
        url = self.ac_url + "/Permissions/{id}".format(id=permission_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return Permission.from_dict(response.json())
        return None

    def get_all_roles(self) -> List[Role]:
        url = self.ac_url + "/Roles"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [Role.from_dict(item) for item in response.json()]
        return []

    def get_role_id_by_name(
        self, name: Union[str, List[str]]
    ) -> Union[int, List[int], None]:
        all_roles = self.get_all_roles()

        if isinstance(name, str):
            names = [name]
        elif isinstance(name, list):
            names = name
        else:
            return None

        roles = [item for item in all_roles if item.name in names]

        if not roles:
            return None
        if len(roles) == 1:
            return roles[0].id
        return [role.id for role in roles]

    def create_new_role(self, name: str, description: str, permission_ids: List[int]) -> bool:
        req = RoleRequest(name=name, description=description, permissionIds=permission_ids)
        url = self.ac_url + "/Roles"
        response = self.api_client.call_api(
            "POST", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == CREATED

    def get_role_by_id(self, role_id: int) -> Role:
        url = self.ac_url + "/Roles/{id}".format(id=role_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return Role.from_dict(response.json())
        return None

    def update_a_role(
        self, role_id: int, name: str, description: str, permission_ids: List[int]
    ) -> bool:
        req = RoleRequest(name=name, description=description, permissionIds=permission_ids)
        url = self.ac_url + "/Roles/{id}".format(id=role_id)
        response = self.api_client.call_api(
            "PUT", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == NO_CONTENT

    def delete_a_role(self, role_id: int) -> bool:
        url = self.ac_url + "/Roles/{id}".format(id=role_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def get_all_saml_identity_providers(self) -> List[SAMLIdentityProvider]:
        url = self.ac_url + "/SamlIdentityProviders"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [SAMLIdentityProvider.from_dict(item) for item in response.json()]
        return []

    def create_new_saml_identity_provider(
        self,
        certificate_file_path: str,
        active: bool,
        name: str,
        issuer: str,
        login_url: str,
        logout_url: str,
        error_url: str,
        sign_authn_request: bool,
        authn_request_binding: str,
        is_manual_management: bool,
        default_team_id: int,
        default_role_id: int,
    ) -> bool:
        file_name = os.path.basename(certificate_file_path)
        url = self.ac_url + "/SamlIdentityProviders"
        response = self.api_client.call_api(
            "POST",
            url,
            files={"CertificateFile": (file_name, open(certificate_file_path, "rb"))},
            data={
                "Active": str(active),
                "Name": name,
                "Issuer": issuer,
                "LoginUrl": login_url,
                "LogoutUrl": logout_url,
                "ErrorUrl": error_url,
                "SignAuthnRequest": str(sign_authn_request),
                "AuthnRequestBinding": authn_request_binding,
                "IsManualManagement": str(is_manual_management),
                "DefaultTeamId": str(default_team_id),
                "DefaultRoleId": str(default_role_id),
            },
        )
        return response.status_code == CREATED

    def get_saml_identity_provider_by_id(self, saml_identity_provider_id: int) -> SAMLIdentityProvider:
        url = self.ac_url + "/SamlIdentityProviders/{id}".format(id=saml_identity_provider_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return SAMLIdentityProvider.from_dict(response.json())
        return None

    def update_new_saml_identity_provider(
        self,
        saml_identity_provider_id: int,
        certificate_file: str,
        active: bool,
        name: str,
        issuer: str,
        login_url: str,
        logout_url: str,
        error_url: str,
        sign_authn_request: bool,
        authn_request_binding: str,
        is_manual_management: bool,
        default_team_id: int,
        default_role_id: int,
    ) -> bool:
        file_name = os.path.basename(certificate_file)
        url = self.ac_url + "/SamlIdentityProviders/{id}".format(id=saml_identity_provider_id)
        response = self.api_client.call_api(
            "PUT",
            url,
            files={"CertificateFile": (file_name, open(certificate_file, "rb"))},
            data={
                "Active": str(active),
                "Name": name,
                "Issuer": issuer,
                "LoginUrl": login_url,
                "LogoutUrl": logout_url,
                "ErrorUrl": error_url,
                "SignAuthnRequest": str(sign_authn_request),
                "AuthnRequestBinding": authn_request_binding,
                "IsManualManagement": str(is_manual_management),
                "DefaultTeamId": str(default_team_id),
                "DefaultRoleId": str(default_role_id),
            },
        )
        return response.status_code == NO_CONTENT

    def delete_a_saml_identity_provider(self, saml_identity_provider_id: int) -> bool:
        url = self.ac_url + "/SamlIdentityProviders/{id}".format(id=saml_identity_provider_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def get_details_of_saml_role_mappings(self, saml_identity_provider_id: int = None) -> List[SAMLRoleMapping]:
        url = self.ac_url + "/SamlRoleMappings"
        if saml_identity_provider_id:
            url += "?samlProviderId={}".format(saml_identity_provider_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [SAMLRoleMapping.from_dict(item) for item in response.json()]
        return []

    def set_saml_group_and_role_mapping_details(
        self,
        saml_identity_provider_id: int,
        sample_role_mapping_details: List[dict] = (),
    ) -> bool:
        put_data = json.dumps(
            [
                {"roleName": item.get("roleName"), "samlAttributeValue": item.get("samlAttributeValue")}
                for item in sample_role_mapping_details
            ]
        )
        url = self.ac_url + "/SamlIdentityProviders/{samlProviderId}/RoleMappings".format(
            samlProviderId=saml_identity_provider_id
        )
        response = self.api_client.call_api(
            "PUT", url, data=put_data, headers={"Content-Type": "application/json"}
        )
        return response.status_code == NO_CONTENT

    def get_saml_service_provider_metadata(self) -> bytes:
        url = self.ac_url + "/SamlServiceProvider/metadata"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return response.content
        return None

    def get_saml_service_provider(self) -> SAMLServiceProvider:
        url = self.ac_url + "/SamlServiceProvider"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return SAMLServiceProvider.from_dict(response.json())
        return None

    def update_a_saml_service_provider(
        self, certificate_file: str, certificate_password: str, issuer: str
    ) -> bool:
        file_name = os.path.basename(certificate_file)
        url = self.ac_url + "/SamlServiceProvider"
        response = self.api_client.call_api(
            "PUT",
            url,
            files={"CertificateFile": (file_name, open(certificate_file, "rb"))},
            data={"CertificatePassword": certificate_password, "Issuer": issuer},
        )
        return response.status_code == NO_CONTENT

    def get_details_of_saml_team_mappings(self, saml_identity_provider_id: int = None) -> List[SAMLTeamMapping]:
        url = self.ac_url + "/SamlTeamMappings"
        if saml_identity_provider_id:
            url += "?samlProviderId={}".format(saml_identity_provider_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [SAMLTeamMapping.from_dict(item) for item in response.json()]
        return []

    def set_saml_group_and_team_mapping_details(
        self, saml_identity_provider_id: int, saml_team_mapping_details: List[dict] = ()
    ) -> bool:
        put_data = json.dumps(
            [
                {"teamFullPath": item.get("teamFullPath"), "samlAttributeValue": item.get("samlAttributeValue")}
                for item in saml_team_mapping_details
            ]
        )
        url = self.ac_url + "/SamlIdentityProviders/{id}/TeamMappings".format(id=saml_identity_provider_id)
        response = self.api_client.call_api(
            "PUT", url, data=put_data, headers={"Content-Type": "application/json"}
        )
        return response.status_code == NO_CONTENT

    def get_all_service_providers(self) -> List[ServiceProvider]:
        url = self.ac_url + "/ServiceProviders"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [ServiceProvider.from_dict(item) for item in response.json()]
        return []

    def get_service_provider_by_id(self, service_provider_id: int) -> ServiceProvider:
        url = self.ac_url + "/ServiceProviders/{id}".format(id=service_provider_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return ServiceProvider.from_dict(response.json())
        return None

    def get_all_smtp_settings(self) -> List[SMTPSetting]:
        url = self.ac_url + "/SMTPSettings"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [SMTPSetting.from_dict(item) for item in response.json()]
        return []

    def create_smtp_settings(
        self,
        password: str,
        host: str,
        port: int,
        encryption_type: str,
        from_address: str,
        use_default_credentials: str,
        username: str,
    ) -> bool:
        req = SMTPSettingRequest(
            password=password,
            host=host,
            port=port,
            encryptionType=encryption_type,
            fromAddress=from_address,
            useDefaultCredentials=use_default_credentials,
            username=username,
        )
        url = self.ac_url + "/SMTPSettings"
        response = self.api_client.call_api(
            "POST", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == CREATED

    def get_smtp_settings_by_id(self, smtp_settings_id: int) -> SMTPSetting:
        url = self.ac_url + "/SMTPSettings/{id}".format(id=smtp_settings_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return SMTPSetting.from_dict(response.json())
        return None

    def update_smtp_settings(
        self,
        smtp_settings_id: int,
        password: str,
        host: str,
        port: int,
        encryption_type: str,
        from_address: str,
        use_default_credentials: str,
        username: str,
    ) -> bool:
        req = SMTPSettingRequest(
            password=password,
            host=host,
            port=port,
            encryptionType=encryption_type,
            fromAddress=from_address,
            useDefaultCredentials=use_default_credentials,
            username=username,
        )
        url = self.ac_url + "/SMTPSettings/{id}".format(id=smtp_settings_id)
        response = self.api_client.call_api(
            "PUT", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == NO_CONTENT

    def delete_smtp_settings(self, smtp_settings_id: int) -> bool:
        url = self.ac_url + "/SMTPSettings/{id}".format(id=smtp_settings_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def test_smtp_connection(
        self,
        receiver_email: str,
        password: str,
        host: str,
        port: int,
        encryption_type: str,
        from_address: str,
        use_default_credentials: str,
        username: str,
    ) -> bool:
        req = SMTPSettingRequest(
            recieverEmail=receiver_email,
            password=password,
            host=host,
            port=port,
            encryptionType=encryption_type,
            fromAddress=from_address,
            useDefaultCredentials=use_default_credentials,
            username=username,
        )
        url = self.ac_url + "/SMTPSettings/testconnection"
        response = self.api_client.call_api(
            "POST", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == OK

    def get_all_system_locales(self) -> List[SystemLocale]:
        url = self.ac_url + "/SystemLocales"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [SystemLocale.from_dict(item) for item in response.json()]
        return []

    def get_members_by_team_id(self, team_id: int) -> List[User]:
        url = self.ac_url + "/Teams/{id}/Users".format(id=team_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [User.from_dict(item) for item in response.json()]
        return []

    def update_members_by_team_id(self, team_id: int, user_ids: List[int]) -> bool:
        put_data = json.dumps({"userIds": user_ids})
        url = self.ac_url + "/Teams/{teamId}/Users".format(teamId=team_id)
        response = self.api_client.call_api(
            "PUT", url, data=put_data, headers={"Content-Type": "application/json"}
        )
        return response.status_code == NO_CONTENT

    def add_a_user_to_a_team(self, team_id: int, user_id: int) -> bool:
        url = self.ac_url + "/Teams/{teamId}/Users/{userId}".format(teamId=team_id, userId=user_id)
        response = self.api_client.call_api("POST", url, data=None)
        return response.status_code == NO_CONTENT

    def delete_a_member_from_a_team(self, team_id: int, user_id: int) -> bool:
        url = self.ac_url + "/Teams/{teamId}/Users/{userId}".format(teamId=team_id, userId=user_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def get_all_teams(self) -> List[Team]:
        url = self.ac_url + "/Teams"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [Team.from_dict(item) for item in response.json()]
        return []

    def get_team_id_by_full_name(self, full_name: str) -> int:
        all_teams = self.get_all_teams()
        team = [item for item in all_teams if item.full_name == full_name]
        return team[0].id if team else None

    def create_new_team(self, name: str, parent_id: int) -> bool:
        post_data = json.dumps({"name": name, "parentId": parent_id})
        url = self.ac_url + "/Teams"
        response = self.api_client.call_api(
            "POST", url, data=post_data, headers={"Content-Type": "application/json"}
        )
        return response.status_code == CREATED

    def create_teams_recursively(self, team_full_name: str) -> List[int]:
        result = []
        if isinstance(team_full_name, str) and team_full_name.startswith("/CxServer"):
            teams = team_full_name.split("/")
            length = len(teams)
            parent_team_id = self.get_team_id_by_full_name("/CxServer")
            for index in list(range(2, length)):
                child_team_full_name = "/".join(teams[: index + 1])
                child_team_name = teams[index]
                team_id = self.get_team_id_by_full_name(child_team_full_name)
                if team_id is None:
                    self.create_new_team(child_team_name, parent_team_id)
                    team_id = self.get_team_id_by_full_name(child_team_full_name)
                    result.append(team_id)
                parent_team_id = team_id
        return result

    def get_team_by_id(self, team_id: int) -> Team:
        url = self.ac_url + "/Teams/{id}".format(id=team_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return Team.from_dict(response.json())
        return None

    def update_a_team(self, team_id: int, name: str, parent_id: int) -> bool:
        put_data = json.dumps({"name": name, "parentId": parent_id})
        url = self.ac_url + "/Teams/{id}".format(id=team_id)
        response = self.api_client.call_api(
            "PUT", url, data=put_data, headers={"Content-Type": "application/json"}
        )
        return response.status_code == NO_CONTENT

    def delete_a_team(self, team_id: int) -> bool:
        url = self.ac_url + "/Teams/{id}".format(id=team_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def generate_a_new_token_signing_certificate(self) -> bool:
        url = self.ac_url + "/TokenSigningCertificateGeneration"
        response = self.api_client.call_api("POST", url)
        return response.status_code == CREATED

    def upload_a_new_token_signing_certificate(
        self, certificate_file_path: str, certificate_password: str
    ) -> bool:
        url = self.ac_url + "/TokenSigningCertificate"
        file_name = os.path.basename(certificate_file_path)
        response = self.api_client.call_api(
            "POST",
            url,
            files={
                "CertificateFile": (file_name, open(certificate_file_path, "rb"), "application/zip")
            },
            data={"CertificatePassword": str(certificate_password)},
        )
        return response.status_code == CREATED

    def get_all_users(self) -> List[User]:
        url = self.ac_url + "/Users"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [User.from_dict(item) for item in response.json()]
        return []

    def get_user_id_by_name(self, username: str) -> int:
        all_users = self.get_all_users()
        user = [item for item in all_users if item.username == username]
        return user[0].id if user else None

    def create_new_user(
        self,
        username: str,
        password: str,
        role_ids: List[int],
        team_ids: List[int],
        authentication_provider_id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        cell_phone_number: str,
        job_title: str,
        other: str,
        country: str,
        active: str,
        expiration_date: str,
        allowed_ip_list: str,
        locale_id: int,
    ) -> bool:
        req = UserRequest(
            username=username,
            password=password,
            roleIds=role_ids,
            teamIds=team_ids,
            authenticationProviderId=authentication_provider_id,
            firstName=first_name,
            lastName=last_name,
            email=email,
            phoneNumber=phone_number,
            cellPhoneNumber=cell_phone_number,
            jobTitle=job_title,
            other=other,
            country=country,
            active=active,
            expirationDate=expiration_date,
            allowedIpList=allowed_ip_list,
            localeId=locale_id,
        )
        url = self.ac_url + "/Users"
        response = self.api_client.call_api(
            "POST", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == CREATED

    def get_user_by_id(self, user_id: int) -> User:
        url = self.ac_url + "/Users/{id}".format(id=user_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return User.from_dict(response.json())
        return None

    def update_a_user(
        self,
        user_id: int,
        role_ids: List[int],
        team_ids: List[int],
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        cell_phone_number: str,
        job_title: str,
        other: str,
        country: str,
        active: str,
        expiration_date: str,
        allowed_ip_list: str,
        locale_id: int,
    ) -> bool:
        req = UserRequest(
            roleIds=role_ids,
            teamIds=team_ids,
            firstName=first_name,
            lastName=last_name,
            email=email,
            phoneNumber=phone_number,
            cellPhoneNumber=cell_phone_number,
            jobTitle=job_title,
            other=other,
            country=country,
            active=active,
            expirationDate=expiration_date,
            allowedIpList=allowed_ip_list,
            localeId=locale_id,
        )
        url = self.ac_url + "/Users/{id}".format(id=user_id)
        response = self.api_client.call_api(
            "PUT", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == NO_CONTENT

    def delete_a_user(self, user_id: int) -> bool:
        url = self.ac_url + "/Users/{id}".format(id=user_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def migrate_existing_user(
        self,
        creation_date: str,
        username: str,
        password: str,
        role_ids: List[str],
        team_ids: List[str],
        authentication_provider_id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        cell_phone_number: str,
        job_title: str,
        other: str,
        country: str,
        active: str,
        expiration_date: str,
        allowed_ip_list: List[str],
        locale_id: str,
    ) -> bool:
        req = UserRequest(
            creationDate=creation_date,
            username=username,
            password=password,
            roleIds=role_ids,
            teamIds=team_ids,
            authenticationProviderId=authentication_provider_id,
            firstName=first_name,
            lastName=last_name,
            email=email,
            phoneNumber=phone_number,
            cellPhoneNumber=cell_phone_number,
            jobTitle=job_title,
            other=other,
            country=country,
            active=active,
            expirationDate=expiration_date,
            allowedIpList=allowed_ip_list,
            localeId=locale_id,
        )
        url = self.ac_url + "/Users/migration"
        response = self.api_client.call_api(
            "POST", url, data=json.dumps(asdict(req)),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code == CREATED

    def get_all_windows_domains(self) -> List[WindowsDomain]:
        url = self.ac_url + "/WindowsDomains"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [WindowsDomain.from_dict(item) for item in response.json()]
        return []

    def get_windows_domain_id_by_name(self, name: str) -> int:
        windows_domains = self.get_all_windows_domains()
        domains = [item for item in windows_domains if item.name == name]
        return domains[0].id if domains else None

    def create_a_new_windows_domain(self, name: str, full_qualified_name: str) -> bool:
        post_data = json.dumps({"name": name, "FullyQualifiedName": full_qualified_name})
        url = self.ac_url + "/WindowsDomains"
        response = self.api_client.call_api(
            "POST", url, data=post_data, headers={"Content-Type": "application/json"}
        )
        return response.status_code == CREATED

    def get_windows_domain_by_id(self, windows_domain_id: int) -> WindowsDomain:
        url = self.ac_url + "/WindowsDomains/{id}".format(id=windows_domain_id)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return WindowsDomain.from_dict(response.json())
        return None

    def update_a_windows_domain(
        self, windows_domain_id: int, name: str, full_qualified_name: str
    ) -> bool:
        put_data = json.dumps({"name": name, "fullyQualifiedName": full_qualified_name})
        url = self.ac_url + "/WindowsDomains/{id}".format(id=windows_domain_id)
        response = self.api_client.call_api(
            "PUT", url, data=put_data, headers={"Content-Type": "application/json"}
        )
        return response.status_code == NO_CONTENT

    def delete_a_windows_domain(self, windows_domain_id: int) -> bool:
        url = self.ac_url + "/WindowsDomains/{id}".format(id=windows_domain_id)
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == NO_CONTENT

    def get_windows_domain_user_entries_by_search_criteria(
        self, windows_domain_id: int, contains_pattern: str = None
    ) -> List[User]:
        url = self.ac_url + "/WindowsDomains/{id}/UserEntries".format(id=windows_domain_id)
        if contains_pattern:
            url += "?containsPattern={}".format(contains_pattern)
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            return [User.from_dict(item) for item in response.json()]
        return []
