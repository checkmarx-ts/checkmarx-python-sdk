from CheckmarxPythonSDK.api_client import ApiClient
import os
import json
from typing import List, Union
from requests_toolbelt import MultipartEncoder

from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT, CREATED
from .accesscontrol.dto import (
    User, AuthenticationProvider, MyProfile, Permission, Role, ServiceProvider, SMTPSetting, SystemLocale, Team,
    WindowsDomain, SAMLIdentityProvider, SAMLServiceProvider, OIDCClient, LDAPRoleMapping, LDAPGroup, LDAPServer,
    LDAPTeamMapping, SAMLRoleMapping, SAMLTeamMapping
)


def construct_user(item):
    return User(
        user_id=item.get("id"),
        username=item.get("userName"),
        last_login_date=item.get("lastLoginDate"),
        role_ids=item.get("roleIds"),
        team_ids=item.get("teamIds"),
        authentication_provider_id=item.get("authenticationProviderId"),
        creation_date=item.get("creationDate"),
        first_name=item.get("firstName"),
        last_name=item.get("lastName"),
        email=item.get("email"),
        phone_number=item.get("phoneNumber"),
        cell_phone_number=item.get("cellPhoneNumber"),
        job_title=item.get("jobTitle"),
        other=item.get("other"),
        country=item.get("country"),
        active=item.get("active"),
        expiration_date=item.get("expirationDate"),
        allowed_ip_list=item.get("allowedIpList"),
        locale_id=item.get("localeId")
    )


class AccessControl:

    def __init__(self, api_client: ApiClient = None, is_iam: bool = False):
        """

        Args:
            api_client (ApiClient):
            is_iam (bool)
        """
        self.api_client = api_client
        self.is_iam = is_iam
        self.sast_ac = "" if is_iam else "/cxrestapi/auth"

    def get_all_assignable_users(self) -> List[User]:
        """

        Returns:
            list[User]
        """
        relative_url = self.sast_ac + "/AssignableUsers"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        return [construct_user(item) for item in response.json() or []]

    def get_all_authentication_providers(self) -> List[AuthenticationProvider]:
        """

        Returns:
            List[AuthenticationProvider]
        """
        result = []
        relative_url = self.sast_ac + "/AuthenticationProviders"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                AuthenticationProvider(
                    authentication_provider_id=item.get("id"),
                    name=item.get("name"),
                    provider_id=item.get("providerId"),
                    provider_type=item.get("providerType"),
                    is_external=item.get("isExternal"),
                    active=item.get("active")
                ) for item in response.json()
            ]
        return result

    def submit_first_admin_user(
            self, username: str, password: str, first_name: str, last_name: str, email: str
    ) -> bool:
        """

        Args:
            username (str):
            password (str):
            first_name (str):
            last_name (str):
            email (str):

        Returns:
            bool
        """
        result = False
        post_data = json.dumps({
            "username": username,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        })
        relative_url = self.sast_ac + "/Users/FirstAdmin"
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        if response.status_code == CREATED:
            result = True
        return result

    def get_admin_user_exists_confirmation(self) -> bool:
        """

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/Users/FirstAdminExistence"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK and response.json().get("firstAdminExists"):
            result = True
        return result

    def get_all_ldap_role_mapping(self, ldap_server_id: int = None) -> List[LDAPRoleMapping]:
        """

        Args:
            ldap_server_id (int):

        Returns:
            List[LDAPRoleMapping]
        """
        result = []
        relative_url = self.sast_ac + "/LDAPRoleMappings"
        if ldap_server_id:
            relative_url += "?ldapServerId={id}".format(id=ldap_server_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                LDAPRoleMapping(
                    ldap_role_mapping_id=item.get("id"),
                    ldap_server_id=item.get("ldapServerId"),
                    role_id=item.get("roleId"),
                    ldap_group_dn=item.get("ldapGroupDn"),
                    ldap_group_display_name=item.get("ldapGroupDisplayName")
                ) for item in response.json()
            ]
        return result

    def update_ldap_role_mapping(
            self, ldap_server_id: int, role_id: int, ldap_group_dn: str, ldap_group_display_name: str
    ) -> bool:
        """

        Args:
            ldap_server_id (int):
            role_id (int):
            ldap_group_dn (str):
            ldap_group_display_name (str):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/LDAPServers/{id}/RoleMappings".format(id=ldap_server_id)
        put_data = json.dumps(
            {
                "roleId": role_id,
                "ldapGroupDn": ldap_group_dn,
                "ldapGroupDisplayName": ldap_group_display_name
            }
        )
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def delete_ldap_role_mapping(self, ldap_role_mapping_id: int) -> bool:
        """

        Args:
            ldap_role_mapping_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/LDAPRoleMappings/{id}".format(id=ldap_role_mapping_id)
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def test_ldap_server_connection(
            self, host: str, port: int, username: str, password: str, use_ssl: bool, verify_ssl_certificate: bool,
            base_dn: str, user_object_filter: str, user_object_class: str, username_attribute: str,
            first_name_attribute: str, last_name_attribute: str, email_attribute: str, synchronization_enabled: bool,
            advanced_team_and_role_mapping_enabled: bool, additional_group_dn: str, group_object_class: str,
            group_object_filter: str, group_name_attribute: str, group_members_attribute: str,
            user_membership_attribute: str
    ) -> bool:
        """

        Args:
            host (str):
            port (int):
            username (str):
            password (str):
            use_ssl (bool):
            verify_ssl_certificate (bool):
            base_dn (str):
            user_object_filter (str):
            user_object_class (str):
            username_attribute (str):
            first_name_attribute (str):
            last_name_attribute (str):
            email_attribute (str):
            synchronization_enabled (bool):
            advanced_team_and_role_mapping_enabled (bool):
            additional_group_dn (str):
            group_object_class (str):
            group_object_filter (str):
            group_name_attribute (str):
            group_members_attribute (str):
            user_membership_attribute (str):

        Returns:
            bool
        """
        post_data = json.dumps(
            {
                "host": host,
                "port": port,
                "username": username,
                "password": password,
                "useSsl": use_ssl,
                "verifySslCertificate": verify_ssl_certificate,
                "baseDn": base_dn,
                "userObjectFilter": user_object_filter,
                "userObjectClass": user_object_class,
                "usernameAttribute": username_attribute,
                "firstNameAttribute": first_name_attribute,
                "lastNameAttribute": last_name_attribute,
                "emailAttribute": email_attribute,
                "synchronizationEnabled": synchronization_enabled,
                "advancedTeamAndRoleMappingEnabled": advanced_team_and_role_mapping_enabled,
                "additionalGroupDn": additional_group_dn,
                "groupObjectClass": group_object_class,
                "groupObjectFilter": group_object_filter,
                "groupNameAttribute": group_name_attribute,
                "groupMembersAttribute": group_members_attribute,
                "userMembershipAttribute": user_membership_attribute
            }
        )
        relative_url = self.sast_ac + "/LDAPServers/TestConnection"
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        return response.status_code == OK

    def get_user_entries_by_search_criteria(
            self, ldap_server_id: int, username_contains_pattern: str = None
    ) -> List[User]:
        """

        Args:
            ldap_server_id (int):
            username_contains_pattern (str):

        Returns:
            List[User]
        """
        result = []
        relative_url = self.sast_ac + "/LDAPServers/{id}/UserEntries".format(id=ldap_server_id)
        if username_contains_pattern:
            relative_url += "?userNameContainsPattern={}".format(username_contains_pattern)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                # We can't use construct_user because the response
                # property names are slightly different (e.g.,
                # "firstname" instead of "firstName".
                User(email=item["email"],
                     first_name=item["firstname"],
                     last_name=item["lastname"],
                     username=item["username"]
                     ) for item in response.json()
            ]
        return result

    def get_group_entries_by_search_criteria(self, ldap_server_id: int, name_contains_pattern: str) -> List[LDAPGroup]:
        """

        Args:
            ldap_server_id (int):
            name_contains_pattern (str):

        Returns:
            List[LDAPGroup]
        """
        result = []
        relative_url = self.sast_ac + "/LDAPServers/{id}/GroupEntries".format(id=ldap_server_id)
        if name_contains_pattern:
            relative_url += "?nameContainsPattern={}".format(name_contains_pattern)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                LDAPGroup(
                    name=item.get("name"),
                    dn=item.get("dn")
                ) for item in response.json()
            ]
        return result

    def get_all_ldap_servers(self) -> List[LDAPServer]:
        """

        Returns:
            List[LDAPServer]
        """
        result = []
        relative_url = self.sast_ac + "/LDAPServers"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                LDAPServer(
                    ldap_server_id=item.get("id"),
                    active=item.get("active"),
                    name=item.get("name"),
                    host=item.get("host"),
                    port=item.get("port"),
                    username=item.get("username"),
                    use_ssl=item.get("useSsl"),
                    verify_ssl_certificate=item.get("verifySslCertificate"),
                    ldap_directory_type=item.get("ldapDirectoryType"),
                    sso_enabled=item.get("ssoEnabled"),
                    mapped_domain_id=item.get("mappedDomainId"),
                    based_dn=item.get("baseDn"),
                    additional_user_dn=item.get("additionalUserDn"),
                    user_object_filter=item.get("userObjectFilter"),
                    user_object_class=item.get("userObjectClass"),
                    username_attribute=item.get("usernameAttribute"),
                    first_name_attribute=item.get("firstNameAttribute"),
                    last_name_attribute=item.get("lastNameAttribute"),
                    email_attribute=item.get("emailAttribute"),
                    synchronization_enabled=item.get("synchronizationEnabled"),
                    default_team_id=item.get("defaultTeamId"),
                    default_role_id=item.get("defaultRoleId"),
                    update_team_and_role_upon_login_enabled=item.get("updateTeamAndRoleUponLoginEnabled"),
                    periodical_synchronization_enabled=item.get("periodicalSynchronizationEnabled"),
                    advanced_team_and_role_mapping_enabled=item.get("advancedTeamAndRoleMappingEnabled"),
                    additional_group_dn=item.get("additionalGroupDn"),
                    group_object_class=item.get("groupObjectClass"),
                    group_object_filter=item.get("groupObjectFilter"),
                    group_name_attribute=item.get("groupNameAttribute"),
                    group_members_attribute=item.get("groupMembersAttribute"),
                    user_membership_attribute=item.get("userMembershipAttribute")
                ) for item in response.json()
            ]
        return result

    def create_new_ldap_server(
            self, password: str, active: bool, name: str, host: str, port: int, username: str, use_ssl: bool,
            verify_ssl_certificate: bool, based_dn: str, additional_user_dn: str, user_object_filter: str,
            user_object_class: str, username_attribute: str, first_name_attribute: str, last_name_attribute: str,
            email_attribute: str, ldap_directory_type: str, sso_enabled: bool, synchronization_enabled: bool,
            default_team_id: int, default_role_id: int, update_team_and_role_upon_login_enabled: bool,
            periodical_synchronization_enabled: bool, advanced_team_and_role_mapping_enabled: bool,
            additional_group_dn: str, group_object_class: str, group_object_filter: str, group_name_attribute: str,
            group_members_attribute: str, user_membership_attribute: str
    ) -> bool:
        """

        Args:
            password (str) :
            active (bool) :
            name (str):
            host (str):
            port (int):
            username (str):
            use_ssl (bool):
            verify_ssl_certificate (bool):
            based_dn (str):
            additional_user_dn (str):
            user_object_filter (str):
            user_object_class (str):
            username_attribute (str):
            first_name_attribute (str):
            last_name_attribute (str):
            email_attribute (str):
            ldap_directory_type (str):
            sso_enabled (bool):
            synchronization_enabled (bool):
            default_team_id (int):
            default_role_id (int):
            update_team_and_role_upon_login_enabled (bool):
            periodical_synchronization_enabled (bool):
            advanced_team_and_role_mapping_enabled (bool):
            additional_group_dn (str):
            group_object_class (str):
            group_object_filter (str):
            group_name_attribute (str):
            group_members_attribute (str):
            user_membership_attribute (str):

        Returns:
            bool
        """
        relative_url = self.sast_ac + "/LDAPServers"
        post_data = json.dumps(
            {
                "password": password,
                "active": active,
                "name": name,
                "host": host,
                "port": port,
                "username": username,
                "useSsl": use_ssl,
                "verifySslCertificate": verify_ssl_certificate,
                "baseDn": based_dn,
                "additionalUserDn": additional_user_dn,
                "userObjectFilter": user_object_filter,
                "userObjectClass": user_object_class,
                "usernameAttribute": username_attribute,
                "firstNameAttribute": first_name_attribute,
                "lastNameAttribute": last_name_attribute,
                "emailAttribute": email_attribute,
                "ldapDirectoryType": ldap_directory_type,
                "ssoEnabled": sso_enabled,
                "synchronizationEnabled": synchronization_enabled,
                "defaultTeamId": default_team_id,
                "defaultRoleId": default_role_id,
                "updateTeamAndRoleUponLoginEnabled": update_team_and_role_upon_login_enabled,
                "periodicalSynchronizationEnabled": periodical_synchronization_enabled,
                "advancedTeamAndRoleMappingEnabled": advanced_team_and_role_mapping_enabled,
                "additionalGroupDn": additional_group_dn,
                "groupObjectClass": group_object_class,
                "groupObjectFilter": group_object_filter,
                "groupNameAttribute": group_name_attribute,
                "groupMembersAttribute": group_members_attribute,
                "userMembershipAttribute": user_membership_attribute
            }
        )
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        return response.status_code == CREATED

    def get_ldap_server_by_id(self, ldap_server_id: int) -> LDAPServer:
        """

        Args:
            ldap_server_id (int):

        Returns:
            LDAPServer
        """
        result = None
        relative_url = self.sast_ac + "/LDAPServers/{id}".format(id=ldap_server_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = LDAPServer(
                ldap_server_id=item.get("id"),
                active=item.get("active"),
                name=item.get("name"),
                host=item.get("host"),
                port=item.get("port"),
                username=item.get("username"),
                use_ssl=item.get("useSsl"),
                verify_ssl_certificate=item.get("verifySslCertificate"),
                ldap_directory_type=item.get("ldapDirectoryType"),
                sso_enabled=item.get("ssoEnabled"),
                mapped_domain_id=item.get("mappedDomainId"),
                based_dn=item.get("baseDn"),
                additional_user_dn=item.get("additionalUserDn"),
                user_object_filter=item.get("userObjectFilter"),
                user_object_class=item.get("userObjectClass"),
                username_attribute=item.get("usernameAttribute"),
                first_name_attribute=item.get("firstNameAttribute"),
                last_name_attribute=item.get("lastNameAttribute"),
                email_attribute=item.get("emailAttribute"),
                synchronization_enabled=item.get("synchronizationEnabled"),
                default_team_id=item.get("defaultTeamId"),
                default_role_id=item.get("defaultRoleId"),
                update_team_and_role_upon_login_enabled=item.get("updateTeamAndRoleUponLoginEnabled"),
                periodical_synchronization_enabled=item.get("periodicalSynchronizationEnabled"),
                advanced_team_and_role_mapping_enabled=item.get("advancedTeamAndRoleMappingEnabled"),
                additional_group_dn=item.get("additionalGroupDn"),
                group_object_class=item.get("groupObjectClass"),
                group_object_filter=item.get("groupObjectFilter"),
                group_name_attribute=item.get("groupNameAttribute"),
                group_members_attribute=item.get("groupMembersAttribute"),
                user_membership_attribute=item.get("userMembershipAttribute")
            )
        return result

    def update_ldap_server(
            self, ldap_server_id: int, password: str, active: bool, name: str, host: str, port: int, username: str,
            use_ssl: bool, verify_ssl_certificate: bool, based_dn: str, additional_user_dn: str, user_object_filter: str,
            user_object_class: str, username_attribute: str, first_name_attribute: str, last_name_attribute: str,
            email_attribute: str, ldap_directory_type: str, sso_enabled: bool, synchronization_enabled: bool,
            default_team_id: str, default_role_id: str, update_team_and_role_upon_login_enabled: bool,
            periodical_synchronization_enabled: bool, advanced_team_and_role_mapping_enabled: bool,
            additional_group_dn: str, group_object_class: str, group_object_filter: str, group_name_attribute: str,
            group_members_attribute: str, user_membership_attribute: str
    ) -> bool:
        """

        Args:
            ldap_server_id (int) :
            password (str) :
            active (bool) :
            name (str):
            host (str):
            port (int):
            username (str):
            use_ssl (bool):
            verify_ssl_certificate (bool):
            based_dn (str):
            additional_user_dn (str):
            user_object_filter (str):
            user_object_class (str):
            username_attribute (str):
            first_name_attribute (str):
            last_name_attribute (str):
            email_attribute (str):
            ldap_directory_type (str):
            sso_enabled (bool):
            synchronization_enabled (bool):
            default_team_id (int):
            default_role_id (int):
            update_team_and_role_upon_login_enabled (bool):
            periodical_synchronization_enabled (bool):
            advanced_team_and_role_mapping_enabled (bool):
            additional_group_dn (str):
            group_object_class (str):
            group_object_filter (str):
            group_name_attribute (str):
            group_members_attribute (str):
            user_membership_attribute (str):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/LDAPServers/{id}".format(id=ldap_server_id)
        put_data = json.dumps(
            {
                "password": password,
                "active": active,
                "name": name,
                "host": host,
                "port": port,
                "username": username,
                "useSsl": use_ssl,
                "verifySslCertificate": verify_ssl_certificate,
                "baseDn": based_dn,
                "additionalUserDn": additional_user_dn,
                "userObjectFilter": user_object_filter,
                "userObjectClass": user_object_class,
                "usernameAttribute": username_attribute,
                "firstNameAttribute": first_name_attribute,
                "lastNameAttribute": last_name_attribute,
                "emailAttribute": email_attribute,
                "ldapDirectoryType": ldap_directory_type,
                "ssoEnabled": sso_enabled,
                "synchronizationEnabled": synchronization_enabled,
                "defaultTeamId": default_team_id,
                "defaultRoleId": default_role_id,
                "updateTeamAndRoleUponLoginEnabled": update_team_and_role_upon_login_enabled,
                "periodicalSynchronizationEnabled": periodical_synchronization_enabled,
                "advancedTeamAndRoleMappingEnabled": advanced_team_and_role_mapping_enabled,
                "additionalGroupDn": additional_group_dn,
                "groupObjectClass": group_object_class,
                "groupObjectFilter": group_object_filter,
                "groupNameAttribute": group_name_attribute,
                "groupMembersAttribute": group_members_attribute,
                "userMembershipAttribute": user_membership_attribute
            }
        )
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def delete_ldap_server(self, ldap_server_id: int) -> bool:
        """

        Args:
            ldap_server_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/LDAPServers/{id}".format(id=ldap_server_id)
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def get_ldap_team_mapping(self, ldap_server_id: int = None, team_id: int = None) -> List[LDAPTeamMapping]:
        """

        Args:
            ldap_server_id (int):
            team_id (int):

        Returns:
            List[LDAPTeamMapping]
        """
        result = []
        relative_url = self.sast_ac + "/LDAPTeamMappings"
        optionals = []
        if ldap_server_id:
            optionals.append("ldapServerId={id}".format(id=ldap_server_id))
        if team_id:
            optionals.append("teamId={id}".format(id=team_id))
        if optionals:
            relative_url += "?" + "&".join(optionals)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                LDAPTeamMapping(
                    ldap_team_mapping_id=item.get("id"),
                    ldap_server_id=item.get("ldapServerId"),
                    team_id=item.get("teamId"),
                    ldap_group_dn=item.get("ldapGroupDn"),
                    ldap_group_display_name=item.get("ldapGroupDisplayName")
                ) for item in response.json()
            ]
        return result

    def update_ldap_team_mapping(
            self, ldap_server_id: int, team_id: int, ldap_group_dn: str, ldap_group_display_name: str
    ) -> bool:
        """

        Args:
            ldap_server_id (int):
            team_id (int):
            ldap_group_dn (str):
            ldap_group_display_name (str):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/LDAPServers/{id}/TeamMappings".format(id=ldap_server_id)
        put_data = json.dumps(
            {
                "teamId": team_id,
                "ldapGroupDn": ldap_group_dn,
                "ldapGroupDisplayName": ldap_group_display_name
            }
        )
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def delete_ldap_team_mapping(self, ldap_team_mapping_id: int) -> bool:
        """

        Args:
            ldap_team_mapping_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/LDAPTeamMappings/{id}".format(id=ldap_team_mapping_id)
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def get_my_profile(self) -> MyProfile:
        """

        Returns:
            MyProfile
        """
        result = None
        relative_url = self.sast_ac + "/MyProfile"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = MyProfile(
                profile_id=item.get("id"),
                username=item.get("userName"),
                first_name=item.get("firstName"),
                last_name=item.get("lastName"),
                email=item.get("email"),
                phone_number=item.get("phoneNumber"),
                cellphone_number=item.get("cellPhoneNumber"),
                job_title=item.get("jobTitle"),
                other=item.get("other"),
                country=item.get("country"),
                locale_id=item.get("localeId"),
                teams=item.get("teams"),
                authentication_provider_id=item.get("authenticationProviderId")
            )
        return result

    def update_my_profile(
            self, first_name: str, last_name: str, email: str, phone_number: str, cell_phone_number: str,
            job_title: str, other: str, country: str, locale_id: int
    ) -> bool:
        """

        Args:
            first_name (str):
            last_name (str):
            email (str):
            phone_number (str):
            cell_phone_number (str):
            job_title (str):
            other (str):
            country (str):
            locale_id (int):

        Returns:
            boolean
        """
        result = False
        put_data = json.dumps({
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phoneNumber": phone_number,
            "cellPhoneNumber": cell_phone_number,
            "jobTitle": job_title,
            "other": other,
            "country": country,
            "localeId": locale_id
        })
        relative_url = self.sast_ac + "/MyProfile"
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def get_all_oidc_clients(self) -> List[OIDCClient]:
        """

        Returns:
            List[OIDCClient]
        """
        result = []
        relative_url = self.sast_ac + "/OIDCClients"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                OIDCClient(
                    oidc_client_id=item.get("id"),
                    update_access_token_claims_on_refresh=item.get("updateAccessTokenClaimsOnRefresh"),
                    access_token_type=item.get("accessTokenType"),
                    include_jwt_id=item.get("includeJwtId"),
                    always_include_user_claims_in_id_token=item.get("alwaysIncludeUserClaimsInIdToken"),
                    client_id=item.get("clientId"),
                    client_name=item.get("clientName"),
                    allow_offline_access=item.get("allowOfflineAccess"),
                    client_secrets=item.get("clientSecrets"),
                    allow_grant_types=item.get("allowedGrantTypes"),
                    allowed_scopes=item.get("allowedScopes"),
                    enabled=item.get("enabled"),
                    require_client_secret=item.get("requireClientSecret"),
                    redirect_uris=item.get("redirectUris"),
                    post_logout_redrect_uris=item.get("postLogoutRedirectUris"),
                    front_channel_logout_uri=item.get("frontChannelLogoutUri"),
                    front_channel_logout_session_required=item.get("frontChannelLogoutSessionRequired"),
                    back_channel_logout_uri=item.get("backChannelLogoutUri"),
                    back_channel_logout_session_required=item.get("backChannelLogoutSessionRequired"),
                    identity_token_life_time=item.get("identityTokenLifetime"),
                    access_token_life_time=item.get("accessTokenLifetime"),
                    authorization_code_life_time=item.get("authorizationCodeLifetime"),
                    absolute_refresh_token_life_time=item.get("absoluteRefreshTokenLifetime"),
                    sliding_refresh_token_life_time=item.get("slidingRefreshTokenLifetime"),
                    refresh_token_usage=item.get("refreshTokenUsage"),
                    refresh_token_expiration=item.get("refreshTokenExpiration"),
                    allowed_cors_origins=item.get("allowedCorsOrigins"),
                    allowed_access_tokens_via_browser=item.get("allowAccessTokensViaBrowser"),
                    claims=item.get("claims"),
                    client_claims_prefix=item.get("clientClaimsPrefix")
                ) for item in response.json()
            ]
        return result

    def create_new_oidc_client(
            self, update_access_token_claims_on_refresh: bool, access_token_type: int, include_jwt_id: bool,
            always_include_user_claims_in_id_token: bool, client_id: str, client_name: str, allow_offline_access: bool,
            client_secrets: List[str], allow_grant_types: List[str], allowed_scopes: List[str], enabled: bool,
            require_client_secret: bool, redirect_uris: List[str], post_logout_redirect_uris: List[str],
            front_channel_logout_uri: str, front_channel_logout_session_required: bool,
            back_channel_logout_uri: str, back_channel_logout_session_required: bool, identity_token_life_time: int,
            access_token_life_time: int, authorization_code_life_time: int, absolute_refresh_token_life_time: int,
            sliding_refresh_token_life_time: int, refresh_token_usage: int, refresh_token_expiration: int,
            allowed_cors_origins: List[str], allowed_access_tokens_via_browser: bool,
            claims: List[str], client_claims_prefix: str
    ) -> bool:
        """

        Args:
            update_access_token_claims_on_refresh (bool):
            access_token_type (int):
            include_jwt_id (bool):
            always_include_user_claims_in_id_token (bool):
            client_id (str):
            client_name (str):
            allow_offline_access (bool):
            client_secrets (list[str]):
            allow_grant_types (list[str]):
            allowed_scopes (list[str]):
            enabled (bool):
            require_client_secret (bool):
            redirect_uris (list):
            post_logout_redirect_uris (list):
            front_channel_logout_uri (str):
            front_channel_logout_session_required (bool):
            back_channel_logout_uri (str):
            back_channel_logout_session_required (bool):
            identity_token_life_time (int):
            access_token_life_time (int):
            authorization_code_life_time (int):
            absolute_refresh_token_life_time (int):
            sliding_refresh_token_life_time (int):
            refresh_token_usage (int):
            refresh_token_expiration (int):
            allowed_cors_origins (list):
            allowed_access_tokens_via_browser (bool):
            claims (list):
            client_claims_prefix (str):

        Returns:
            bool
        """
        result = False
        post_data = json.dumps(
            {
                "updateAccessTokenClaimsOnRefresh": update_access_token_claims_on_refresh,
                "accessTokenType": access_token_type,
                "includeJwtId": include_jwt_id,
                "alwaysIncludeUserClaimsInIdToken": always_include_user_claims_in_id_token,
                "clientId": client_id,
                "clientName": client_name,
                "allowOfflineAccess": allow_offline_access,
                "clientSecrets": client_secrets,
                "allowedGrantTypes": allow_grant_types,
                "allowedScopes": allowed_scopes,
                "enabled": enabled,
                "requireClientSecret": require_client_secret,
                "redirectUris": redirect_uris,
                "postLogoutRedirectUris": post_logout_redirect_uris,
                "frontChannelLogoutUri": front_channel_logout_uri,
                "frontChannelLogoutSessionRequired": front_channel_logout_session_required,
                "backChannelLogoutUri": back_channel_logout_uri,
                "backChannelLogoutSessionRequired": back_channel_logout_session_required,
                "identityTokenLifetime": identity_token_life_time,
                "accessTokenLifetime": access_token_life_time,
                "authorizationCodeLifetime": authorization_code_life_time,
                "absoluteRefreshTokenLifetime": absolute_refresh_token_life_time,
                "slidingRefreshTokenLifetime": sliding_refresh_token_life_time,
                "refreshTokenUsage": refresh_token_usage,
                "refreshTokenExpiration": refresh_token_expiration,
                "allowedCorsOrigins": allowed_cors_origins,
                "allowAccessTokensViaBrowser": allowed_access_tokens_via_browser,
                "claims": claims,
                "clientClaimsPrefix": client_claims_prefix
            }
        )
        relative_url = self.sast_ac + "/OIDCClients"
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        if response.status_code == CREATED:
            result = True
        return result

    def get_oidc_client_by_id(self, oidc_client_id: int) -> OIDCClient:
        """

        Args:
            oidc_client_id (int):

        Returns:
            OIDCClient
        """
        result = None
        relative_url = self.sast_ac + "/OIDCClients/{id}".format(id=oidc_client_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = OIDCClient(
                oidc_client_id=item.get("id"),
                update_access_token_claims_on_refresh=item.get("updateAccessTokenClaimsOnRefresh"),
                access_token_type=item.get("accessTokenType"),
                include_jwt_id=item.get("includeJwtId"),
                always_include_user_claims_in_id_token=item.get("alwaysIncludeUserClaimsInIdToken"),
                client_id=item.get("clientId"),
                client_name=item.get("clientName"),
                allow_offline_access=item.get("allowOfflineAccess"),
                client_secrets=item.get("clientSecrets"),
                allow_grant_types=item.get("allowedGrantTypes"),
                allowed_scopes=item.get("allowedScopes"),
                enabled=item.get("enabled"),
                require_client_secret=item.get("requireClientSecret"),
                redirect_uris=item.get("redirectUris"),
                post_logout_redrect_uris=item.get("postLogoutRedirectUris"),
                front_channel_logout_uri=item.get("frontChannelLogoutUri"),
                front_channel_logout_session_required=item.get("frontChannelLogoutSessionRequired"),
                back_channel_logout_uri=item.get("backChannelLogoutUri"),
                back_channel_logout_session_required=item.get("backChannelLogoutSessionRequired"),
                identity_token_life_time=item.get("identityTokenLifetime"),
                access_token_life_time=item.get("accessTokenLifetime"),
                authorization_code_life_time=item.get("authorizationCodeLifetime"),
                absolute_refresh_token_life_time=item.get("absoluteRefreshTokenLifetime"),
                sliding_refresh_token_life_time=item.get("slidingRefreshTokenLifetime"),
                refresh_token_usage=item.get("refreshTokenUsage"),
                refresh_token_expiration=item.get("refreshTokenExpiration"),
                allowed_cors_origins=item.get("allowedCorsOrigins"),
                allowed_access_tokens_via_browser=item.get("allowAccessTokensViaBrowser"),
                claims=item.get("claims"),
                client_claims_prefix=item.get("clientClaimsPrefix")
            )
        return result

    def update_an_oidc_client(
            self, oidc_client_id: int, update_access_token_claims_on_refresh: bool, access_token_type: int,
            include_jwt_id: bool, always_include_user_claims_in_id_token: bool, client_id: str, client_name: str,
            allow_offline_access: bool, client_secrets: List[str], allow_grant_types: List[str],
            allowed_scopes: List[str], enabled: bool, require_client_secret: bool,
            redirect_uris: List[str], post_logout_redirect_uris: List[str], front_channel_logout_uri: str,
            front_channel_logout_session_required: bool, back_channel_logout_uri: str,
            back_channel_logout_session_required: bool, identity_token_life_time: int,
            access_token_life_time: int, authorization_code_life_time: int, absolute_refresh_token_life_time: int,
            sliding_refresh_token_life_time: int, refresh_token_usage: int, refresh_token_expiration: int,
            allowed_cors_origins: List[str], allowed_access_tokens_via_browser: bool,
            claims: List[str], client_claims_prefix: str
    ) -> bool:
        """

        Args:
            oidc_client_id (int):
            update_access_token_claims_on_refresh (bool):
            access_token_type (int):
            include_jwt_id (bool):
            always_include_user_claims_in_id_token (bool):
            client_id (str):
            client_name (str):
            allow_offline_access (bool):
            client_secrets (list[str]):
            allow_grant_types (list[str]):
            allowed_scopes (list[str]):
            enabled (bool):
            require_client_secret (bool):
            redirect_uris (list):
            post_logout_redirect_uris (list):
            front_channel_logout_uri (str):
            front_channel_logout_session_required (bool):
            back_channel_logout_uri (str):
            back_channel_logout_session_required (bool):
            identity_token_life_time (int):
            access_token_life_time (int):
            authorization_code_life_time (int):
            absolute_refresh_token_life_time (int):
            sliding_refresh_token_life_time (int):
            refresh_token_usage (int):
            refresh_token_expiration (int):
            allowed_cors_origins (list):
            allowed_access_tokens_via_browser (bool):
            claims (list):
            client_claims_prefix (str):

        Returns:
            bool
        """
        result = False
        put_data = json.dumps(
            {
                "updateAccessTokenClaimsOnRefresh": update_access_token_claims_on_refresh,
                "accessTokenType": access_token_type,
                "includeJwtId": include_jwt_id,
                "alwaysIncludeUserClaimsInIdToken": always_include_user_claims_in_id_token,
                "clientId": client_id,
                "clientName": client_name,
                "allowOfflineAccess": allow_offline_access,
                "clientSecrets": client_secrets,
                "allowedGrantTypes": allow_grant_types,
                "allowedScopes": allowed_scopes,
                "enabled": enabled,
                "requireClientSecret": require_client_secret,
                "redirectUris": redirect_uris,
                "postLogoutRedirectUris": post_logout_redirect_uris,
                "frontChannelLogoutUri": front_channel_logout_uri,
                "frontChannelLogoutSessionRequired": front_channel_logout_session_required,
                "backChannelLogoutUri": back_channel_logout_uri,
                "backChannelLogoutSessionRequired": back_channel_logout_session_required,
                "identityTokenLifetime": identity_token_life_time,
                "accessTokenLifetime": access_token_life_time,
                "authorizationCodeLifetime": authorization_code_life_time,
                "absoluteRefreshTokenLifetime": absolute_refresh_token_life_time,
                "slidingRefreshTokenLifetime": sliding_refresh_token_life_time,
                "refreshTokenUsage": refresh_token_usage,
                "refreshTokenExpiration": refresh_token_expiration,
                "allowedCorsOrigins": allowed_cors_origins,
                "allowAccessTokensViaBrowser": allowed_access_tokens_via_browser,
                "claims": claims,
                "clientClaimsPrefix": client_claims_prefix
            }
        )

        relative_url = self.sast_ac + "/OIDCClients/{id}".format(id=oidc_client_id)
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def delete_an_oidc_client(self, oidc_client_id: int) -> bool:
        """

        Args:
            oidc_client_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/OIDCClients/{id}".format(id=oidc_client_id)
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def get_all_permissions(self) -> List[Permission]:
        """

        Returns:
            List[Permission]
        """
        result = []
        relative_url = self.sast_ac + "/Permissions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                Permission(
                    permission_id=item.get("id"),
                    service_provider_id=item.get("serviceProviderId"),
                    name=item.get("name"),
                    category=item.get("category"),
                ) for item in response.json()
            ]
        return result

    def get_permission_by_id(self, permission_id: int) -> Permission:
        """

        Args:
            permission_id (int):

        Returns:
            Permission
        """
        result = None
        relative_url = self.sast_ac + "/Permissions/{id}".format(id=permission_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = Permission(
                permission_id=item.get("id"),
                service_provider_id=item.get("serviceProviderId"),
                name=item.get("name"),
                category=item.get("category")
            )
        return result

    def get_all_roles(self) -> List[Role]:
        """

        Returns:
            List[Role]
        """
        result = []
        relative_url = self.sast_ac + "/Roles"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                Role(
                    role_id=item.get("id"),
                    is_system_role=item.get("isSystemRole"),
                    name=item.get("name"),
                    description=item.get("description"),
                    permission_ids=item.get("permissionIds")
                ) for item in response.json()
            ]
        return result

    def get_role_id_by_name(self, name: Union[str, List[str]]) -> Union[int, List[int], None]:
        """

        Args:
            name (str, list of str):

        Returns:
            int, list of int
        """

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

        if len(roles) > 1:
            return [role.id for role in roles]

    def create_new_role(self, name: str, description: str, permission_ids: List[int]) -> bool:
        """

        Args:
            name (str):
            description (str):
            permission_ids (list of int):

        Returns:
            boolean
        """
        post_data = json.dumps(
            {
                "name": name,
                "description": description,
                "permissionIds": permission_ids
            }
        )
        relative_url = self.sast_ac + "/Roles"
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        return response.status_code == CREATED

    def get_role_by_id(self, role_id: int) -> Role:
        """

        Args:
            role_id (int): unique id of the role

        Returns:
            Role
        """
        result = None
        relative_url = self.sast_ac + "/Roles/{id}".format(id=role_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = Role(
                role_id=item.get("id"),
                is_system_role=item.get("isSystemRole"),
                name=item.get("name"),
                description=item.get("description"),
                permission_ids=item.get("permissionIds")
            )
        return result

    def update_a_role(self, role_id: int, name: str, description: str, permission_ids: List[int]) -> bool:
        """

        Args:
            role_id (int):
            name (str):
            description (str):
            permission_ids (list[int]):

        Returns:
            Boolean
        """
        result = False
        put_data = json.dumps(
            {
                "name": name,
                "description": description,
                "permissionIds": permission_ids
            }
        )
        relative_url = self.sast_ac + "/Roles/{id}".format(id=role_id)
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def delete_a_role(self, role_id: int) -> bool:
        """

        Args:
            role_id (int):

        Returns:
            Boolean
        """
        result = False
        relative_url = self.sast_ac + "/Roles/{id}".format(id=role_id)
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def get_all_saml_identity_providers(self) -> List[SAMLIdentityProvider]:
        """

        Returns:
            List[SAMLIdentityProvider]
        """
        result = []
        relative_url = self.sast_ac + "/SamlIdentityProviders"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                SAMLIdentityProvider(
                    saml_identity_provider_id=item.get("id"),
                    certificate_file_name=item.get("certificateFileName"),
                    certificate_subject=item.get("certificateSubject"),
                    active=item.get("active"),
                    name=item.get("name"),
                    issuer=item.get("issuer"),
                    login_url=item.get("loginUrl"),
                    logout_url=item.get("logoutUrl"),
                    error_url=item.get("errorUrl"),
                    sign_authn_request=item.get("signAuthnRequest"),
                    authn_request_binding=item.get("authnRequestBinding"),
                    is_manual_management=item.get("isManualManagement"),
                    default_team_id=item.get("defaultTeamId"),
                    default_role_id=item.get("defaultRoleId")
                ) for item in response.json()
            ]
        return result

    def create_new_saml_identity_provider(
            self, certificate_file_path: str, active: bool, name: str, issuer: str, login_url: str, logout_url: str,
            error_url: str, sign_authn_request: bool, authn_request_binding: str, is_manual_management: bool,
            default_team_id: int, default_role_id: int
    ) -> bool:
        """

        Args:
            certificate_file_path (str):
            active (bool):
            name (str):
            issuer (str):
            login_url (str):
            logout_url (str, None):
            error_url (str, None):
            sign_authn_request (bool):
            authn_request_binding (str):
            is_manual_management (bool):
            default_team_id (int):
            default_role_id (int):

        Returns:
            bool
        """
        result = False
        file_name = os.path.basename(certificate_file_path)
        m = MultipartEncoder(
            fields={
                "CertificateFile": (file_name, open(certificate_file_path, 'r')),
                "Active": active,
                "Name": name,
                "Issuer": issuer,
                "LoginUrl": login_url,
                "LogoutUrl": logout_url,
                "ErrorUrl": error_url,
                "SignAuthnRequest": sign_authn_request,
                "AuthnRequestBinding": authn_request_binding,
                "IsManualManagement": is_manual_management,
                "DefaultTeamId": default_team_id,
                "DefaultRoleId": default_role_id
            }
        )
        headers = {"Content-Type": m.content_type}
        relative_url = self.sast_ac + "/SamlIdentityProviders"
        response = self.api_client.post_request(relative_url=relative_url, data=m, headers=headers, is_iam=self.is_iam)
        return response.status_code == CREATED

    def get_saml_identity_provider_by_id(self, saml_identity_provider_id: int) -> SAMLIdentityProvider:
        """

        Args:
            saml_identity_provider_id (int):

        Returns:
            SAMLIdentityProvider
        """
        result = None
        relative_url = self.sast_ac + "/SamlIdentityProviders/{id}".format(id=saml_identity_provider_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = SAMLIdentityProvider(
                saml_identity_provider_id=item.get("id"),
                certificate_file_name=item.get("certificateFileName"),
                certificate_subject=item.get("certificateSubject"),
                active=item.get("active"),
                name=item.get("name"),
                issuer=item.get("issuer"),
                login_url=item.get("loginUrl"),
                logout_url=item.get("logoutUrl"),
                error_url=item.get("errorUrl"),
                sign_authn_request=item.get("signAuthnRequest"),
                authn_request_binding=item.get("authnRequestBinding"),
                is_manual_management=item.get("isManualManagement"),
                default_team_id=item.get("defaultTeamId"),
                default_role_id=item.get("defaultRoleId")
            )
        return result

    def update_new_saml_identity_provider(
            self, saml_identity_provider_id: int, certificate_file: str, active: bool, name: str, issuer: str,
            login_url: str, logout_url: str, error_url: str, sign_authn_request: bool, authn_request_binding: str,
            is_manual_management: bool, default_team_id: int, default_role_id: int
    ) -> bool:
        """

        Args:
            saml_identity_provider_id (int):
            certificate_file (str):
            active (bool):
            name (str):
            issuer (str):
            login_url (str):
            logout_url (str):
            error_url (str):
            sign_authn_request (bool):
            authn_request_binding (str):
            is_manual_management (bool):
            default_team_id (int):
            default_role_id (int):

        Returns:
            bool
        """
        result = False
        file_name = os.path.basename(certificate_file)
        m = MultipartEncoder(
            fields={
                "CertificateFile": (file_name, open(certificate_file, 'r')),
                "Active": active,
                "Name": name,
                "Issuer": issuer,
                "LoginUrl": login_url,
                "LogoutUrl": logout_url,
                "ErrorUrl": error_url,
                "SignAuthnRequest": sign_authn_request,
                "AuthnRequestBinding": authn_request_binding,
                "IsManualManagement": is_manual_management,
                "DefaultTeamId": default_team_id,
                "DefaultRoleId": default_role_id
            }
        )
        headers = {"Content-Type": m.content_type}
        relative_url = self.sast_ac + "/SamlIdentityProviders/{id}".format(id=saml_identity_provider_id)
        response = self.api_client.put_request(relative_url=relative_url, data=m, headers=headers, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def delete_a_saml_identity_provider(self, saml_identity_provider_id: int) -> bool:
        """

        Args:
            saml_identity_provider_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/SamlIdentityProviders/{id}".format(id=saml_identity_provider_id)
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def get_details_of_saml_role_mappings(self, saml_identity_provider_id: int = None) -> List[SAMLRoleMapping]:
        """

        Args:
            saml_identity_provider_id (int):

        Returns:
            `list` of `SAMLRoleMapping`
        """
        result = []
        relative_url = self.sast_ac + "/SamlRoleMappings"
        if saml_identity_provider_id:
            relative_url += "?samlProviderId={}".format(saml_identity_provider_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                SAMLRoleMapping(
                    saml_role_mapping_id=item.get('id'),
                    saml_identity_provider_id=item.get('samlIdentityProviderId'),
                    role_id=item.get('roleId'),
                    role_name=item.get('roleName'),
                    saml_attribute_value=item.get('samlAttributeValue')
                ) for item in response.json()
            ]
        return result

    def set_saml_group_and_role_mapping_details(
            self, saml_identity_provider_id: int, sample_role_mapping_details: List[dict]=()
    ) -> bool:
        """

        Args:
            saml_identity_provider_id (int):
            sample_role_mapping_details (`list` of dict):
            [
              {
                "roleName": "string",
                "samlAttributeValue": "string"
              }
            ]

        Returns:
            bool
        """
        result = False
        put_data = json.dumps(
            [
                {
                    "roleName": item.get("roleName"),
                    "samlAttributeValue": item.get("samlAttributeValue")
                }
                for item in sample_role_mapping_details
            ]
        )
        relative_url = self.sast_ac + "/SamlIdentityProviders/{samlProviderId}/RoleMappings".format(
            samlProviderId=saml_identity_provider_id
        )
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def get_saml_service_provider_metadata(self) -> bytes:
        """

        Returns:
            byte
        """
        result = None
        relative_url = self.sast_ac + "/SamlServiceProvider/metadata"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = response.content
        return result

    def get_saml_service_provider(self) -> SAMLServiceProvider:
        """

        Returns:
            SAMLServiceProvider
        """
        result = None
        relative_url = self.sast_ac + "/SamlServiceProvider"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = SAMLServiceProvider(
                assertion_consumer_service_url=item.get("assertionConsumerServiceUrl"),
                certificate_file_name=item.get("certificateFileName"),
                certificate_subject=item.get("certificateSubject"),
                issuer=item.get("issuer")
            )
        return result

    def update_a_saml_service_provider(
            self, certificate_file: str, certificate_password: str, issuer: str
    ) -> bool:
        """

        Args:

            certificate_file (str):
            certificate_password (str):
            issuer (str):

        Returns:
            bool
        """
        result = False
        file_name = os.path.basename(certificate_file)
        m = MultipartEncoder(
            fields={
                "CertificateFile": (file_name, open(certificate_file, 'rb')),
                "CertificatePassword": certificate_password,
                "Issuer": issuer
            }
        )
        headers = {"Content-Type": m.content_type}
        relative_url = self.sast_ac + "/SamlServiceProvider"
        response = self.api_client.put_request(relative_url=relative_url, data=m, headers=headers, is_iam=self.is_iam)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def get_details_of_saml_team_mappings(self, saml_identity_provider_id: int = None) -> List[SAMLTeamMapping]:
        """

        Args:
            saml_identity_provider_id (int):

        Returns:
            List[SAMLTeamMapping]
        """
        result = []
        relative_url = self.sast_ac + "/SamlTeamMappings"
        if saml_identity_provider_id:
            relative_url += "?samlProviderId={}".format(saml_identity_provider_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                SAMLTeamMapping(
                    saml_team_mapping_id=item.get("id"),
                    saml_identity_provider_id=item.get("samlIdentityProviderId"),
                    team_id=item.get("teamId"),
                    team_full_path=item.get("teamFullPath"),
                    saml_attribute_value=item.get("samlAttributeValue")
                ) for item in response.json()
            ]
        return result

    def set_saml_group_and_team_mapping_details(
            self, saml_identity_provider_id: int, saml_team_mapping_details: List[dict] = ()
    ) -> bool:
        """

        Args:
            saml_identity_provider_id (int):
            saml_team_mapping_details (`list` of dict):
                [
                  {
                    "teamFullPath": "string",
                    "samlAttributeValue": "string"
                  }
                ]
        Returns:
            bool
        """
        result = False
        put_data = json.dumps(
            [
                {
                    "teamFullPath": item.get("teamFullPath"),
                    "samlAttributeValue": item.get("samlAttributeValue")
                }
                for item in saml_team_mapping_details
            ]
        )
        relative_url = self.sast_ac + "/SamlIdentityProviders/{id}/TeamMappings".format(
            id=saml_identity_provider_id
        )
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def get_all_service_providers(self) -> List[ServiceProvider]:
        """
        access control 2.0
        Returns:
            List[ServiceProvider]
        """
        result = []
        relative_url = self.sast_ac + "/ServiceProviders"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                ServiceProvider(
                    service_provider_id=item.get("id"),
                    name=item.get("name")
                ) for item in response.json()
            ]
        return result

    def get_service_provider_by_id(self, service_provider_id: int) -> ServiceProvider:
        """

        Args:
            service_provider_id (int):

        Returns:
            ServiceProvider
        """
        result = None
        relative_url = self.sast_ac + "/ServiceProviders/{id}".format(id=service_provider_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = ServiceProvider(
                service_provider_id=item.get("id"),
                name=item.get("name")
            )
        return result

    def get_all_smtp_settings(self) -> List[SMTPSetting]:
        """

        Returns:
            List[SMTPSetting]
        """
        result = []
        relative_url = self.sast_ac + "/SMTPSettings"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                SMTPSetting(
                    smtp_settings_id=item.get("id"),
                    host=item.get("host"),
                    port=item.get("port"),
                    encryption_type=item.get("encryptionType"),
                    from_address=item.get("fromAddress"),
                    use_default_credentials=item.get("useDefaultCredentials"),
                    username=item.get("username")
                ) for item in response.json()
            ]
        return result

    def create_smtp_settings(
            self, password: str, host: str, port: int, encryption_type: str, from_address: str,
            use_default_credentials: str, username: str
    ) -> bool:
        """

        Args:
            password (str):
            host (str):
            port (int):
            encryption_type (str):
            from_address (str):
            use_default_credentials (str):
            username (str):

        Returns:
            bool
        """
        result = False
        post_data = json.dumps(
            {
                "password": password,
                "host": host,
                "port": port,
                "encryptionType": encryption_type,
                "fromAddress": from_address,
                "useDefaultCredentials": use_default_credentials,
                "username": username
            }
        )
        relative_url = self.sast_ac + "/SMTPSettings"
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        return response.status_code == CREATED

    def get_smtp_settings_by_id(self, smtp_settings_id: int) -> SMTPSetting:
        """

        Args:
            smtp_settings_id (int):

        Returns:
            SMTPSetting
        """
        result = None
        relative_url = self.sast_ac + "/SMTPSettings/{id}".format(id=smtp_settings_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = SMTPSetting(
                smtp_settings_id=item.get("id"),
                host=item.get("host"),
                port=item.get("port"),
                encryption_type=item.get("encryptionType"),
                from_address=item.get("fromAddress"),
                use_default_credentials=item.get("useDefaultCredentials"),
                username=item.get("username")
            )
        return result

    def update_smtp_settings(
            self, smtp_settings_id: int, password: str, host: str, port: int, encryption_type: str, from_address: str,
            use_default_credentials: str, username: str
    ) -> bool:
        """

        Args:
            smtp_settings_id (int):
            password (str):
            host (str):
            port (int):
            encryption_type (str):
            from_address (str):
            use_default_credentials (str):
            username (str):

        Returns:
            bool
        """
        result = False
        put_data = json.dumps(
            {
                "password": password,
                "host": host,
                "port": port,
                "encryptionType": encryption_type,
                "fromAddress": from_address,
                "useDefaultCredentials": use_default_credentials,
                "username": username
            }
        )
        relative_url = self.sast_ac + "/SMTPSettings/{id}".format(id=smtp_settings_id)
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def delete_smtp_settings(self, smtp_settings_id: int) -> bool:
        """

        Args:
            smtp_settings_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/SMTPSettings/{id}".format(id=smtp_settings_id)
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def test_smtp_connection(
            self, receiver_email: str, password: str, host: str, port: int, encryption_type: str, from_address: str,
            use_default_credentials: str, username: str
    ) -> bool:
        """

        Args:
            receiver_email (str):
            password (str):
            host (str):
            port (int):
            encryption_type (str):
            from_address (str):
            use_default_credentials (str):
            username (str):

        Returns:
            bool
        """
        result = False
        post_data = json.dumps(
            {
                "recieverEmail": receiver_email,
                "password": password,
                "host": host,
                "port": port,
                "encryptionType": encryption_type,
                "fromAddress": from_address,
                "useDefaultCredentials": use_default_credentials,
                "username": username
            }
        )
        relative_url = self.sast_ac + "/SMTPSettings/testconnection"
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        return response.status_code == OK

    def get_all_system_locales(self) -> List[SystemLocale]:
        """

        Returns:
            List[SystemLocale]
        """
        result = []
        relative_url = self.sast_ac + "/SystemLocales"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                SystemLocale(
                    system_locale_id=item.get("id"),
                    lcid=item.get("lcid"),
                    code=item.get("code"),
                    display_name=item.get("displayName")
                ) for item in response.json()
            ]
        return result

    def get_members_by_team_id(self, team_id: int) -> List[User]:
        """

        Args:
            team_id (int):

        Returns:
            List[User]
        """
        result = []
        relative_url = self.sast_ac + "/Teams/{id}/Users".format(id=team_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                construct_user(item) for item in response.json()
            ]
        return result

    def update_members_by_team_id(self, team_id: int, user_ids: List[int]) -> int:
        """

        Args:
            team_id (int):
            user_ids (list[int]):

        Returns:
            bool
        """
        result = False
        put_data = json.dumps(
            {"userIds": user_ids}
        )
        relative_url = self.sast_ac + "/Teams/{teamId}/Users".format(teamId=team_id)
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def add_a_user_to_a_team(self, team_id: int, user_id: int) -> bool:
        """

        Args:
            team_id (int):
            user_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/Teams/{teamId}/Users/{userId}".format(
            teamId=team_id, userId=user_id
        )
        response = self.api_client.post_request(relative_url=relative_url, data=None, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def delete_a_member_from_a_team(self, team_id: int, user_id: int) -> bool:
        """

        Args:
            team_id (int):
            user_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/Teams/{teamId}/Users/{userId}".format(
            teamId=team_id,
            userId=user_id
        )
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def get_all_teams(self) -> List[Team]:
        """

        Returns:
            List[Team]
        """
        result = []
        relative_url = self.sast_ac + "/Teams"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                Team(
                    team_id=item.get("id"),
                    name=item.get("name"),
                    full_name=item.get("fullName"),
                    parent_id=item.get("parentId")
                ) for item in response.json()
            ]
        return result

    def get_team_id_by_full_name(self, full_name: str) -> int:
        """

        Args:
            full_name (str):

        Returns:
            int
        """
        team_id = None

        all_teams = self.get_all_teams()

        team = [item for item in all_teams if item.full_name == full_name]
        if team:
            team_id = team[0].id

        return team_id

    def create_new_team(self, name: str, parent_id: int) -> bool:
        """

        Args:
            name (str):
            parent_id (int):

        Returns:
            bool
        """
        result = False
        post_data = json.dumps(
            {
                "name": name,
                "parentId": parent_id
            }
        )
        relative_url = self.sast_ac + "/Teams"
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        return response.status_code == CREATED

    def create_teams_recursively(self, team_full_name: str) -> List[int]:
        """
        create new team by team full name recursively. Check the team existence start from root team /CxServer
        Args:
            team_full_name (str):

        Returns:
            List[int]
        """
        result = []
        if isinstance(team_full_name, str) and team_full_name.startswith("/CxServer"):
            teams = team_full_name.split("/")
            length = len(teams)
            parent_team_id = self.get_team_id_by_full_name("/CxServer")
            for index in list(range(2, length)):
                child_team_full_name = "/".join(teams[:index+1])
                child_team_name = teams[index]
                team_id = self.get_team_id_by_full_name(child_team_full_name)
                if team_id is None:
                    self.create_new_team(child_team_name, parent_team_id)
                    team_id = self.get_team_id_by_full_name(child_team_full_name)
                    result.append(team_id)
                parent_team_id = team_id

        return result

    def get_team_by_id(self, team_id: int) -> Team:
        """

        Args:
            team_id(int):

        Returns:
            Team
        """
        result = None
        relative_url = self.sast_ac + "/Teams/{id}".format(id=team_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = Team(
                team_id=item.get("id"),
                name=item.get("name"),
                full_name=item.get("fullName"),
                parent_id=item.get("parentId")
            )
        return result

    def update_a_team(self, team_id: int, name: str, parent_id: int) -> bool:
        """

        Args:
            team_id (int):
            name (str):
            parent_id (int):

        Returns:
            bool
        """
        result = False
        put_data = json.dumps(
            {
                "name": name,
                "parentId": parent_id
            }
        )
        relative_url = self.sast_ac + "/Teams/{id}".format(id=team_id)
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def delete_a_team(self, team_id: int) -> bool:
        """

        Args:
            team_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/Teams/{id}".format(id=team_id)
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def generate_a_new_token_signing_certificate(self) -> bool:
        """

        Returns:
            bool
        """
        relative_url = self.sast_ac + "/TokenSigningCertificateGeneration"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=self.is_iam)
        return response.status_code == CREATED

    def upload_a_new_token_signing_certificate(self, certificate_file_path: str, certificate_password: str) -> bool:
        """

        Args:
            certificate_file_path (str):
            certificate_password (str):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/TokenSigningCertificate"
        file_name = os.path.basename(certificate_file_path)
        m = MultipartEncoder(
            fields={
                "CertificateFile": (file_name, open(certificate_file_path, 'rb'), "application/zip"),
                "CertificatePassword": str(certificate_password)
            }
        )
        headers = {"Content-Type": m.content_type}
        response = self.api_client.post_request(relative_url=relative_url, data=m, headers=headers, is_iam=self.is_iam)
        return response.status_code == CREATED

    def get_all_users(self) -> List[User]:
        """

        Returns:
            List[User]
        """
        result = []
        relative_url = self.sast_ac + "/Users"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                construct_user(item) for item in response.json()
            ]
        return result

    def get_user_id_by_name(self, username: str) -> int:
        """

        Args:
            username (str):

        Returns:
            int
        """
        user_id = None

        all_users = self.get_all_users()
        user = [item for item in all_users if item.username == username]
        if user:
            user_id = user[0].id
        return user_id

    def create_new_user(
            self, username: str, password: str, role_ids: List[int], team_ids: List[int],
            authentication_provider_id: int, first_name: str, last_name: str, email: str, phone_number: str,
            cell_phone_number: str, job_title: str, other: str, country: str, active: str,
            expiration_date: str, allowed_ip_list: str, locale_id: int
    ) -> bool:
        """

        Args:
            username (str): required
            password (str): required
            role_ids (list[int], None):
            team_ids (list[int]): required.   user must be a member of at least one team
            authentication_provider_id (int):  1, application
            first_name (str): required
            last_name (str): required
            email (str): required
            phone_number (str, None):
            cell_phone_number (str, None):
            job_title (str, None):
            other (str, None):
            country (str, None):
            active (str): true/false
            expiration_date (str):
            allowed_ip_list (str, None):
            locale_id (int):

        Returns:
            bool
        """
        result = False
        post_data = json.dumps(
            {
                "username": username,
                "password": password,
                "roleIds": role_ids,
                "teamIds": team_ids,
                "authenticationProviderId": authentication_provider_id,
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "phoneNumber": phone_number,
                "cellPhoneNumber": cell_phone_number,
                "jobTitle": job_title,
                "other": other,
                "country": country,
                "active": active,
                "expirationDate": expiration_date,
                "allowedIpList": allowed_ip_list,
                "localeId": locale_id
            }
        )
        relative_url = self.sast_ac + "/Users"
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        return response.status_code == CREATED

    def get_user_by_id(self, user_id: int) -> User:
        """

        Args:
            user_id (int):

        Returns:
            User
        """
        result = None
        relative_url = self.sast_ac + "/Users/{id}".format(id=user_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = construct_user(item)
        return result

    def update_a_user(
            self, user_id: int, role_ids: List[int], team_ids: List[int], first_name: str, last_name: str, email: str,
            phone_number: str, cell_phone_number: str, job_title: str, other: str, country: str, active: str,
            expiration_date: str, allowed_ip_list: str, locale_id: int
    ) -> bool:
        """

        Args:
            user_id (int):
            role_ids (list[int]):
            team_ids (list[int]):
            first_name (str):
            last_name (str):
            email (str):
            phone_number (str, None):
            cell_phone_number (str, None):
            job_title (str, None):
            other (str, None):
            country (str, None):
            active (str): true/false
            expiration_date (str):
            allowed_ip_list (str, None):
            locale_id (int):

        Returns:
            bool
        """
        result = False
        put_data = json.dumps(
            {
                "roleIds": role_ids,
                "teamIds": team_ids,
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "phoneNumber": phone_number,
                "cellPhoneNumber": cell_phone_number,
                "jobTitle": job_title,
                "other": other,
                "country": country,
                "active": active,
                "expirationDate": expiration_date,
                "allowedIpList": allowed_ip_list,
                "localeId": locale_id
            }
        )
        relative_url = self.sast_ac + "/Users/{id}".format(id=user_id)
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def delete_a_user(self, user_id: int) -> bool:
        """

        Args:
            user_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/Users/{id}".format(id=user_id)
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def migrate_existing_user(
            self, creation_date: str, username: str, password: str, role_ids: List[str], team_ids: List[str],
            authentication_provider_id: int, first_name: str, last_name: str, email: str, phone_number: str,
            cell_phone_number: str, job_title: str, other: str, country: str, active: str, expiration_date: str,
            allowed_ip_list: List[str], locale_id: str
    ) -> bool:
        """

        Args:
            creation_date:
            username:
            password:
            role_ids:
            team_ids:
            authentication_provider_id:
            first_name:
            last_name:
            email:
            phone_number:
            cell_phone_number:
            job_title:
            other:
            country:
            active:
            expiration_date:
            allowed_ip_list:
            locale_id:

        Returns:
            bool
        """
        result = False
        post_data = json.dumps(
            {
                "creationDate": creation_date,
                "username": username,
                "password": password,
                "roleIds": role_ids,
                "teamIds": team_ids,
                "authenticationProviderId": authentication_provider_id,
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "phoneNumber": phone_number,
                "cellPhoneNumber": cell_phone_number,
                "jobTitle": job_title,
                "other": other,
                "country": country,
                "active": active,
                "expirationDate": expiration_date,
                "allowedIpList": allowed_ip_list,
                "localeId": locale_id
            }
        )
        relative_url = self.sast_ac + "/Users/migration"
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        return response.status_code == CREATED

    def get_all_windows_domains(self) -> List[WindowsDomain]:
        """

        Returns:
            List[WindowsDomain]
        """
        result = []
        relative_url = self.sast_ac + "/WindowsDomains"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                WindowsDomain(
                    windows_domain_id=item.get("id"),
                    name=item.get("name"),
                    full_qualified_name=item.get("fullyQualifiedName")
                ) for item in response.json()
            ]
        return result

    def get_windows_domain_id_by_name(self, name: str) -> int:
        """

        Args:
            name (str):

        Returns:
            int
        """
        windows_domain_id = None

        windows_domains = self.get_all_windows_domains()
        domains = [item for item in windows_domains if item.name == name]
        if domains:
            windows_domain_id = domains[0].id
        return windows_domain_id

    def create_a_new_windows_domain(self, name: str, full_qualified_name: str) -> bool:
        """

        Args:
            name (str):
            full_qualified_name (str):

        Returns:
            bool
        """
        result = False
        post_data = json.dumps(
            {
                "name": name,
                "FullyQualifiedName": full_qualified_name
            }
        )
        relative_url = self.sast_ac + "/WindowsDomains"
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=self.is_iam)
        if response.status_code == CREATED:
            result = True
        return result

    def get_windows_domain_by_id(self, windows_domain_id: int) -> WindowsDomain:
        """

        Args:
            windows_domain_id (int):

        Returns:
            WindowsDomain
        """
        result = None
        relative_url = self.sast_ac + "/WindowsDomains/{id}".format(id=windows_domain_id)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            item = response.json()
            result = WindowsDomain(
                windows_domain_id=item.get("id"),
                name=item.get("name"),
                full_qualified_name=item.get("fullyQualifiedName")
            )
        return result

    def update_a_windows_domain(self, windows_domain_id: int, name: str, full_qualified_name: str) -> bool:
        """

        Args:
            windows_domain_id (int):
            name (str):
            full_qualified_name (str):

        Returns:
            bool
        """
        result = False
        put_data = json.dumps(
            {
                "name": name,
                "fullyQualifiedName": full_qualified_name
            }
        )
        relative_url = self.sast_ac + "/WindowsDomains/{id}".format(id=windows_domain_id)
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def delete_a_windows_domain(self, windows_domain_id: int) -> bool:
        """

        Args:
            windows_domain_id (int):

        Returns:
            bool
        """
        result = False
        relative_url = self.sast_ac + "/WindowsDomains/{id}".format(id=windows_domain_id)
        response = self.api_client.delete_request(relatvie_url=relative_url, is_iam=self.is_iam)
        return response.status_code == NO_CONTENT

    def get_windows_domain_user_entries_by_search_criteria(
            self, windows_domain_id: int, contains_pattern: str = None
    ) -> List[User]:
        """

        Args:
            windows_domain_id (int):
            contains_pattern (str):

        Returns:
            List[User]
        """
        result = []
        relative_url = self.sast_ac + "/WindowsDomains/{id}/UserEntries".format(id=windows_domain_id)
        if contains_pattern:
            relative_url += "?containsPattern={}".format(contains_pattern)
        response = self.api_client.get_request(relative_url=relative_url, is_iam=self.is_iam)
        if response.status_code == OK:
            result = [
                User(
                    username=item.get("username"),
                    first_name=item.get("firstname"),
                    last_name=item.get("lastname"),
                    email=item.get("email")
                ) for item in response.json()
            ]
        return result
