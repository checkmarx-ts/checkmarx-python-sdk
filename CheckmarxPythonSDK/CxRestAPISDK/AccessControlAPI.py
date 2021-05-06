# encoding: utf-8
import os
import requests
import json

from copy import copy

from requests_toolbelt import MultipartEncoder

from ..compat import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, FORBIDDEN, NO_CONTENT, CREATED
from ..config import config

from . import authHeaders
from .exceptions.CxError import BadRequestError, NotFoundError, CxError
from .accesscontrol.dto import (
    User, AuthenticationProvider, MyProfile, Permission, Role, ServiceProvider, SMTPSetting, SystemLocale, Team,
    WindowsDomain, SAMLIdentityProvider, SAMLServiceProvider, OIDCClient, LDAPRoleMapping, LDAPGroup, LDAPServer,
    LDAPTeamMapping
)


class AccessControlAPI(object):

    def __init__(self):
        self.retry = 0

    def get_all_assignable_users(self):
        """

        Returns:
            list[User]
        """

        url = config.get("base_url") + "/cxrestapi/auth/AssignableUsers"

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_list = r.json()
            assignable_users = [
                User(
                    user_id=item.get("id"),
                    username=item.get("username"),
                    first_name=item.get("firstName"),
                    last_name=item.get("lastName"),
                    email=item.get("email")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            assignable_users = self.get_all_assignable_users()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return assignable_users

    def get_all_authentication_providers(self):
        """

        Returns:
            list[AuthenticationProvider]
        """
        url = config.get("base_url") + "/cxrestapi/auth/AuthenticationProviders"

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            authentication_providers = [
                AuthenticationProvider(
                    authentication_provider_id=item.get("id"),
                    name=item.get("name"),
                    provider_id=item.get("providerId"),
                    provider_type=item.get("providerType"),
                    is_external=item.get("isExternal"),
                    active=item.get("active")
                ) for item in a_list
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            authentication_providers = self.get_all_authentication_providers()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return authentication_providers

    def submit_first_admin_user(self, username, password, first_name, last_name, email):
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
        post_data = json.dumps({
            "username": username,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        })

        url = config.get("base_url") + "/cxrestapi/auth/Users/FirstAdmin"
        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.submit_first_admin_user(username, password, first_name, last_name, email)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_admin_user_exists_confirmation(self):

        first_admin_exists = False

        url = config.get("base_url") + "/cxrestapi/auth/Users/FirstAdminExistence"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            if item.get("firstAdminExists"):
                first_admin_exists = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            first_admin_exists = self.get_admin_user_exists_confirmation()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return first_admin_exists

    def get_all_ldap_role_mapping(self, ldap_server_id=None):
        """

        Args:
            ldap_server_id (int):

        Returns:
            list[LDAPRoleMapping]
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPRoleMappings"
        if ldap_server_id:
            url += "?ldapServerId={id}".format(id=ldap_server_id)

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            ldap_role_mapping = [
                LDAPRoleMapping(
                    ldap_role_mapping_id=item.get("id"),
                    ldap_server_id=item.get("ldapServerId"),
                    role_id=item.get("roleId"),
                    ldap_group_dn=item.get("ldapGroupDn"),
                    ldap_group_display_name=item.get("ldapGroupDisplayName")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            ldap_role_mapping = self.get_all_ldap_role_mapping()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return ldap_role_mapping

    def update_ldap_role_mapping(self, ldap_server_id, role_id, ldap_group_dn, ldap_group_display_name):
        """

        Args:
            ldap_server_id (int):
            role_id (int):
            ldap_group_dn (str):
            ldap_group_display_name (str):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPServers/{id}/RoleMappings".format(id=ldap_server_id)

        put_data = json.dumps(
            {
                "roleId": role_id,
                "ldapGroupDn": ldap_group_dn,
                "ldapGroupDisplayName": ldap_group_display_name
            }
        )

        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_ldap_role_mapping(ldap_server_id, role_id, ldap_group_dn,
                                                          ldap_group_display_name)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_ldap_role_mapping(self, ldap_role_mapping_id):
        """

        Args:
            ldap_role_mapping_id (int):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPRoleMappings/{id}".format(id=ldap_role_mapping_id)

        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_ldap_role_mapping(ldap_role_mapping_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def test_ldap_server_connection(self, host, port, username, password, use_ssl, verify_ssl_certificate, base_dn,
                                    user_object_filter, user_object_class, username_attribute, first_name_attribute,
                                    last_name_attribute, email_attribute, synchronization_enabled,
                                    advanced_team_and_role_mapping_enabled, additional_group_dn, group_object_class,
                                    group_object_filter, group_name_attribute, group_members_attribute,
                                    user_membership_attribute):
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

        url = config.get("base_url") + "/cxrestapi/auth/LDAPServers/TestConnection"

        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.test_ldap_server_connection(host, port, username, password, use_ssl,
                                                             verify_ssl_certificate, base_dn,
                                                             user_object_filter, user_object_class, username_attribute,
                                                             first_name_attribute,
                                                             last_name_attribute, email_attribute,
                                                             synchronization_enabled,
                                                             advanced_team_and_role_mapping_enabled,
                                                             additional_group_dn,
                                                             group_object_class,
                                                             group_object_filter, group_name_attribute,
                                                             group_members_attribute,
                                                             user_membership_attribute)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_user_entries_by_search_criteria(self, ldap_server_id, username_contains_pattern=None):
        """

        Args:
            ldap_server_id (int):
            username_contains_pattern (str):

        Returns:
            list[User]
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPServers/{id}/UserEntries".format(id=ldap_server_id)
        if username_contains_pattern:
            url += "?userNameContainsPattern={}".format(username_contains_pattern)

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            user_entries = [
                User(
                    username=item.get("username"),
                    first_name=item.get("firstName"),
                    last_name=item.get("lastName"),
                    email=item.get("email")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            user_entries = self.get_user_entries_by_search_criteria(ldap_server_id, username_contains_pattern)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return user_entries

    def get_group_entries_by_search_criteria(self, ldap_server_id, name_contains_pattern):
        """

        Args:
            ldap_server_id (int):
            name_contains_pattern (str):

        Returns:
            list[LDAPGroup]
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPServers/{id}/GroupEntries".format(id=ldap_server_id)
        if name_contains_pattern:
            url += "?nameContainsPattern={}".format(name_contains_pattern)

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            ldap_groups = [
                LDAPGroup(
                    name=item.get("name"),
                    dn=item.get("dn")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            ldap_groups = self.get_group_entries_by_search_criteria(ldap_server_id, name_contains_pattern)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return ldap_groups

    def get_all_ldap_servers(self):
        """

        Returns:
            list[LDAPServer]
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPServers"

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            ldap_servers = [
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
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            ldap_servers = self.get_all_ldap_servers()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return ldap_servers

    def create_new_ldap_server(self, password, active, name, host, port, username, use_ssl, verify_ssl_certificate,
                               based_dn, additional_user_dn, user_object_filter,
                               user_object_class, username_attribute, first_name_attribute, last_name_attribute,
                               email_attribute,
                               ldap_directory_type, sso_enabled,
                               synchronization_enabled, default_team_id, default_role_id,
                               update_team_and_role_upon_login_enabled,
                               periodical_synchronization_enabled, advanced_team_and_role_mapping_enabled,
                               additional_group_dn,
                               group_object_class, group_object_filter, group_name_attribute, group_members_attribute,
                               user_membership_attribute):
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
        url = config.get("base_url") + "/cxrestapi/auth/LDAPServers"

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

        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.create_new_ldap_server(password, active, name, host, port, username, use_ssl,
                                                        verify_ssl_certificate,
                                                        based_dn, additional_user_dn, user_object_filter,
                                                        user_object_class, username_attribute, first_name_attribute,
                                                        last_name_attribute,
                                                        email_attribute,
                                                        ldap_directory_type, sso_enabled,
                                                        synchronization_enabled, default_team_id, default_role_id,
                                                        update_team_and_role_upon_login_enabled,
                                                        periodical_synchronization_enabled,
                                                        advanced_team_and_role_mapping_enabled,
                                                        additional_group_dn,
                                                        group_object_class, group_object_filter, group_name_attribute,
                                                        group_members_attribute,
                                                        user_membership_attribute)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_ldap_server_by_id(self, ldap_server_id):
        """

        Args:
            ldap_server_id (int):

        Returns:
            LDAPServer
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPServers/{id}".format(id=ldap_server_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            ldap_server = LDAPServer(
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
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            ldap_server = self.get_ldap_server_by_id(ldap_server_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return ldap_server

    def update_ldap_server(self, ldap_server_id, password, active, name, host, port, username, use_ssl,
                           verify_ssl_certificate, based_dn, additional_user_dn, user_object_filter,
                           user_object_class, username_attribute, first_name_attribute, last_name_attribute,
                           email_attribute,
                           ldap_directory_type, sso_enabled,
                           synchronization_enabled, default_team_id, default_role_id,
                           update_team_and_role_upon_login_enabled,
                           periodical_synchronization_enabled, advanced_team_and_role_mapping_enabled,
                           additional_group_dn,
                           group_object_class, group_object_filter, group_name_attribute, group_members_attribute,
                           user_membership_attribute):
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
        url = config.get("base_url") + "/cxrestapi/auth/LDAPServers/{id}".format(id=ldap_server_id)

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

        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_ldap_server(ldap_server_id, password, active, name, host, port, username,
                                                    use_ssl,
                                                    verify_ssl_certificate,
                                                    based_dn, additional_user_dn, user_object_filter,
                                                    user_object_class, username_attribute, first_name_attribute,
                                                    last_name_attribute,
                                                    email_attribute,
                                                    ldap_directory_type, sso_enabled,
                                                    synchronization_enabled, default_team_id, default_role_id,
                                                    update_team_and_role_upon_login_enabled,
                                                    periodical_synchronization_enabled,
                                                    advanced_team_and_role_mapping_enabled,
                                                    additional_group_dn,
                                                    group_object_class, group_object_filter, group_name_attribute,
                                                    group_members_attribute,
                                                    user_membership_attribute)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_ldap_server(self, ldap_server_id):
        """

        Args:
            ldap_server_id (int):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPServers/{id}".format(id=ldap_server_id)

        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_ldap_server(ldap_server_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_ldap_team_mapping(self, ldap_server_id=None, team_id=None):
        """

        Args:
            ldap_server_id (int):
            team_id (int):

        Returns:
            list[LDAPTeamMapping]
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPTeamMappings"

        optionals = []
        if ldap_server_id:
            optionals.append("ldapServerId={id}".format(id=ldap_server_id))
        if team_id:
            optionals.append("teamId={id}".format(id=team_id))
        if optionals:
            url += "?" + "&".join(optionals)

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            ldap_team_mapping = [
                LDAPTeamMapping(
                    ldap_team_mapping_id=item.get("id"),
                    ldap_server_id=item.get("ldapServerId"),
                    team_id=item.get("teamId"),
                    ldap_group_dn=item.get("ldapGroupDn"),
                    ldap_group_display_name=item.get("ldapGroupDisplayName")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            ldap_team_mapping = self.get_ldap_team_mapping(ldap_server_id, team_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return ldap_team_mapping

    def update_ldap_team_mapping(self, ldap_server_id, team_id, ldap_group_dn, ldap_group_display_name):
        """

        Args:
            ldap_server_id (int):
            team_id (int):
            ldap_group_dn (str):
            ldap_group_display_name (str):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPServers/{id}/TeamMappings".format(id=ldap_server_id)

        put_data = json.dumps(
            {
                "teamId": team_id,
                "ldapGroupDn": ldap_group_dn,
                "ldapGroupDisplayName": ldap_group_display_name
            }
        )

        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_ldap_team_mapping(ldap_server_id, team_id, ldap_group_dn,
                                                          ldap_group_display_name)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_ldap_team_mapping(self, ldap_team_mapping_id):
        """

        Args:
            ldap_team_mapping_id (int):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/LDAPTeamMappings/{id}".format(id=ldap_team_mapping_id)

        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_ldap_team_mapping(ldap_team_mapping_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_my_profile(self):
        """

        Returns:
            MyProfile
        """
        url = config.get("base_url") + "/cxrestapi/auth/MyProfile"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            my_profile = MyProfile(
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
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            my_profile = self.get_my_profile()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return my_profile

    def update_my_profile(self, first_name, last_name, email, phone_number, cell_phone_number, job_title, other,
                          country, locale_id):
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

        url = config.get("base_url") + "/cxrestapi/auth/MyProfile"
        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_my_profile(first_name, last_name, email, phone_number, cell_phone_number,
                                                   job_title, other,
                                                   country, locale_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_all_oidc_clients(self):
        """

        Returns:
            list[OIDCClient]
        """
        url = config.get("base_url") + "/cxrestapi/auth/OIDCClients"

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_list = r.json()
            oidc_clients = [
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
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            oidc_clients = self.get_all_oidc_clients()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return oidc_clients

    def create_new_oidc_client(self, update_access_token_claims_on_refresh, access_token_type, include_jwt_id,
                               always_include_user_claims_in_id_token, client_id, client_name, allow_offline_access,
                               client_secrets, allow_grant_types, allowed_scopes, enabled, require_client_secret,
                               redirect_uris,
                               post_logout_redrect_uris, front_channel_logout_uri,
                               front_channel_logout_session_required,
                               back_channel_logout_uri, back_channel_logout_session_required, identity_token_life_time,
                               access_token_life_time, authorization_code_life_time, absolute_refresh_token_life_time,
                               sliding_refresh_token_life_time, refresh_token_usage, refresh_token_expiration,
                               allowed_cors_origins,
                               allowed_access_tokens_via_browser, claims, client_claims_prefix):
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
            post_logout_redrect_uris (list):
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
                "postLogoutRedirectUris": post_logout_redrect_uris,
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

        url = config.get("base_url") + "/cxrestapi/auth/OIDCClients"

        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.create_new_oidc_client(update_access_token_claims_on_refresh, access_token_type,
                                                        include_jwt_id,
                                                        always_include_user_claims_in_id_token, client_id, client_name,
                                                        allow_offline_access,
                                                        client_secrets, allow_grant_types, allowed_scopes, enabled,
                                                        require_client_secret, redirect_uris,
                                                        post_logout_redrect_uris, front_channel_logout_uri,
                                                        front_channel_logout_session_required,
                                                        back_channel_logout_uri, back_channel_logout_session_required,
                                                        identity_token_life_time,
                                                        access_token_life_time, authorization_code_life_time,
                                                        absolute_refresh_token_life_time,
                                                        sliding_refresh_token_life_time, refresh_token_usage,
                                                        refresh_token_expiration,
                                                        allowed_cors_origins,
                                                        allowed_access_tokens_via_browser, claims, client_claims_prefix)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_oidc_client_by_id(self, oidc_client_id):
        """

        Args:
            oidc_client_id (int):

        Returns:
            OIDCClient
        """
        url = config.get("base_url") + "/cxrestapi/auth/OIDCClients/{id}".format(id=oidc_client_id)

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            item = r.json()
            oidc_client = OIDCClient(
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
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            oidc_client = self.get_oidc_client_by_id(oidc_client_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return oidc_client

    def update_an_oidc_client(self, oidc_client_id, update_access_token_claims_on_refresh, access_token_type,
                              include_jwt_id,
                              always_include_user_claims_in_id_token, client_id, client_name, allow_offline_access,
                              client_secrets, allow_grant_types, allowed_scopes, enabled, require_client_secret,
                              redirect_uris,
                              post_logout_redrect_uris, front_channel_logout_uri,
                              front_channel_logout_session_required,
                              back_channel_logout_uri, back_channel_logout_session_required, identity_token_life_time,
                              access_token_life_time, authorization_code_life_time, absolute_refresh_token_life_time,
                              sliding_refresh_token_life_time, refresh_token_usage, refresh_token_expiration,
                              allowed_cors_origins,
                              allowed_access_tokens_via_browser, claims, client_claims_prefix):
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
            post_logout_redrect_uris (list):
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
                "postLogoutRedirectUris": post_logout_redrect_uris,
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

        url = config.get("base_url") + "/cxrestapi/auth/OIDCClients/{id}".format(id=oidc_client_id)

        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_an_oidc_client(oidc_client_id, update_access_token_claims_on_refresh,
                                                       access_token_type,
                                                       include_jwt_id,
                                                       always_include_user_claims_in_id_token, client_id, client_name,
                                                       allow_offline_access,
                                                       client_secrets, allow_grant_types, allowed_scopes, enabled,
                                                       require_client_secret, redirect_uris,
                                                       post_logout_redrect_uris, front_channel_logout_uri,
                                                       front_channel_logout_session_required,
                                                       back_channel_logout_uri, back_channel_logout_session_required,
                                                       identity_token_life_time,
                                                       access_token_life_time, authorization_code_life_time,
                                                       absolute_refresh_token_life_time,
                                                       sliding_refresh_token_life_time, refresh_token_usage,
                                                       refresh_token_expiration,
                                                       allowed_cors_origins,
                                                       allowed_access_tokens_via_browser, claims, client_claims_prefix)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_an_oidc_client(self, oidc_client_id):
        """

        Args:
            oidc_client_id (int):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/OIDCClients/{id}".format(id=oidc_client_id)

        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_an_oidc_client(oidc_client_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_all_permissions(self):

        url = config.get("base_url") + "/cxrestapi/auth/Permissions"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            all_permissions = [
                Permission(
                    permission_id=item.get("id"),
                    service_provider_id=item.get("serviceProviderId"),
                    name=item.get("name"),
                    category=item.get("category"),
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            all_permissions = self.get_all_permissions()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_permissions

    def get_permission_by_id(self, permission_id):
        """

        Args:
            permission_id (int):

        Returns:

        """
        url = config.get("base_url") + "/cxrestapi/auth/Permissions/{id}".format(id=permission_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            permission = Permission(
                permission_id=item.get("id"),
                service_provider_id=item.get("serviceProviderId"),
                name=item.get("name"),
                category=item.get("category")
            )
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            permission = self.get_permission_by_id(permission_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return permission

    def get_all_roles(self):

        url = config.get("base_url") + "/cxrestapi/auth/Roles"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            all_roles = [
                Role(
                    role_id=item.get("id"),
                    is_system_role=item.get("isSystemRole"),
                    name=item.get("name"),
                    description=item.get("description"),
                    permission_ids=item.get("permission_ids")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            all_roles = self.get_all_roles()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_roles

    def get_role_id_by_name(self, name):
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

    def create_new_role(self, name, description, permission_ids):
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

        url = config.get("base_url") + "/cxrestapi/auth/Roles"
        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.create_new_role(name, description, permission_ids)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_role_by_id(self, role_id):
        """

        Args:
            role_id (int): unique id of the role

        Returns:
            Role
        """
        url = config.get("base_url") + "/cxrestapi/auth/Roles/{id}".format(id=role_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            role = Role(
                role_id=item.get("id"),
                is_system_role=item.get("isSystemRole"),
                name=item.get("name"),
                description=item.get("description"),
                permission_ids=item.get("permissionIds")
            )
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            role = self.get_role_by_id(role_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return role

    def update_a_role(self, role_id, name, description, permission_ids):
        """

        Args:
            role_id (int):
            name (str):
            description (str):
            permission_ids (list[int]):

        Returns:
            Boolean
        """
        put_data = json.dumps(
            {
                "name": name,
                "description": description,
                "permissionIds": permission_ids
            }
        )

        url = config.get("base_url") + "/cxrestapi/auth/Roles/{id}".format(id=role_id)
        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_a_role(role_id, name, description, permission_ids)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_a_role(self, role_id):
        """

        Args:
            role_id (int):

        Returns:
            Boolean
        """
        url = config.get("base_url") + "/cxrestapi/auth/Roles/{id}".format(id=role_id)
        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_a_role(role_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_all_saml_identity_providers(self):
        """

        Returns:
            list[SAMLIdentityProvider]
        """
        url = config.get("base_url") + "/cxrestapi/auth/SamlIdentityProviders"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            all_saml_identity_providers = [
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
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            all_saml_identity_providers = self.get_all_saml_identity_providers()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_saml_identity_providers

    def create_new_saml_identity_provider(self, certificate_file_path, active, name, issuer, login_url, logout_url,
                                          error_url, sign_authn_request, authn_request_binding, is_manual_management,
                                          default_team_id, default_role_id):
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
        headers = copy(authHeaders.auth_headers)

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
        headers.update({"Content-Type": m.content_type})

        url = config.get("base_url") + "/cxrestapi/auth/SamlIdentityProviders"
        r = requests.post(
            url=url,
            files=m,
            headers=headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.create_new_saml_identity_provider(certificate_file_path, active, name, issuer,
                                                                   login_url, logout_url,
                                                                   error_url, sign_authn_request, authn_request_binding,
                                                                   is_manual_management, default_team_id,
                                                                   default_role_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_saml_identity_provider_by_id(self, saml_identity_provider_id):
        """

        Args:
            saml_identity_provider_id (int):

        Returns:
            SAMLIdentityProvider
        """
        url = config.get("base_url") + "/cxrestapi/auth/SamlIdentityProviders/{id}".format(id=saml_identity_provider_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            saml_identity_provider = SAMLIdentityProvider(
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
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            saml_identity_provider = self.get_saml_identity_provider_by_id(saml_identity_provider_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return saml_identity_provider

    def update_new_saml_identity_provider(self, saml_identity_provider_id, certificate_file, active, name, issuer,
                                          login_url, logout_url, error_url, sign_authn_request, authn_request_binding,
                                          is_manual_management, default_team_id, default_role_id):
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
        put_data = {
            "CertificateFile": open(certificate_file, 'rb'),
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

        headers = copy(authHeaders.auth_headers)

        headers.update(
            {
                "Content-Type": "multipart/form-data;v=1.0",
            }
        )

        url = config.get("base_url") + "/cxrestapi/auth/SamlIdentityProviders/{id}".format(id=saml_identity_provider_id)
        r = requests.put(
            url=url,
            files=put_data,
            headers=headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_new_saml_identity_provider(saml_identity_provider_id, certificate_file, active,
                                                                   name, issuer,
                                                                   login_url, logout_url, error_url, sign_authn_request,
                                                                   authn_request_binding, is_manual_management,
                                                                   default_team_id,
                                                                   default_role_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_a_saml_identity_provider(self, saml_identity_provider_id):
        """

        Args:
            saml_identity_provider_id (int):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/SamlIdentityProviders/{id}".format(id=saml_identity_provider_id)
        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_a_saml_identity_provider(saml_identity_provider_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_saml_service_provider_metadata(self):
        """

        Returns:
            byte
        """
        url = config.get("base_url") + "/cxrestapi/auth/SamlServiceProvider/metadata"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            saml_service_provider_metadata = r.content
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            saml_service_provider_metadata = self.get_saml_service_provider_metadata()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return saml_service_provider_metadata

    def get_saml_service_provider(self):
        """

        Returns:
            SAMLServiceProvider
        """
        url = config.get("base_url") + "/cxrestapi/auth/SamlServiceProvider"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            saml_service_provider = SAMLServiceProvider(
                assertion_consumer_service_url=item.get("assertionConsumerServiceUrl"),
                certificate_file_name=item.get("certificateFileName"),
                certificate_subject=item.get("certificateSubject"),
                issuer=item.get("issuer")
            )
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            saml_service_provider = self.get_saml_service_provider()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return saml_service_provider

    def update_a_saml_service_provider(self, certificate_file, certificate_password, issuer):
        """

        Args:

            certificate_file (str):
            certificate_password (str):
            issuer (str):

        Returns:
            bool
        """
        put_data = {
            "CertificateFile": open(certificate_file, 'rb'),
            "CertificatePassword": certificate_password,
            "Issuer": issuer
        }

        headers = copy(authHeaders.auth_headers)

        headers.update(
            {
                "Content-Type": "multipart/form-data;v=1.0",
            }
        )

        url = config.get("base_url") + "/cxrestapi/auth/SamlServiceProvider"
        r = requests.put(
            url=url,
            files=put_data,
            headers=headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_a_saml_service_provider(certificate_file, certificate_password, issuer)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_all_service_providers(self):
        """
        access control 2.0
        Returns:
            list[ServiceProvider]
        """
        url = config.get("base_url") + "/cxrestapi/auth/ServiceProviders"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            service_providers = [
                ServiceProvider(
                    service_provider_id=item.get("id"),
                    name=item.get("name")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            service_providers = self.get_all_service_providers()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return service_providers

    def get_service_provider_by_id(self, service_provider_id):
        """

        Args:
            service_provider_id (int):

        Returns:
            ServiceProvider
        """
        url = config.get("base_url") + "/cxrestapi/auth/ServiceProviders/{id}".format(id=service_provider_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            service_provider = ServiceProvider(
                service_provider_id=item.get("id"),
                name=item.get("name")
            )
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            service_provider = self.get_service_provider_by_id(service_provider_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return service_provider

    def get_all_smtp_settings(self):
        """

        Returns:
            list[SMTPSetting]
        """
        url = config.get("base_url") + "/cxrestapi/auth/SMTPSettings"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            smtp_settings = [
                SMTPSetting(
                    smtp_settings_id=item.get("id"),
                    host=item.get("host"),
                    port=item.get("port"),
                    encryption_type=item.get("encryptionType"),
                    from_address=item.get("fromAddress"),
                    use_default_credentials=item.get("useDefaultCredentials"),
                    username=item.get("username")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            smtp_settings = self.get_all_smtp_settings()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return smtp_settings

    def create_smtp_settings(self, password, host, port, encryption_type, from_address, use_default_credentials,
                             username):
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
            Boolean
        """
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

        url = config.get("base_url") + "/cxrestapi/auth/SMTPSettings"
        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.create_smtp_settings(password, host, port, encryption_type, from_address,
                                                      use_default_credentials,
                                                      username)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_smtp_settings_by_id(self, smtp_settings_id):
        """

        Args:
            smtp_settings_id (int):

        Returns:
            SMTPSetting
        """
        url = config.get("base_url") + "/cxrestapi/auth/SMTPSettings/{id}".format(id=smtp_settings_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            smtp_setting = SMTPSetting(
                smtp_settings_id=item.get("id"),
                host=item.get("host"),
                port=item.get("port"),
                encryption_type=item.get("encryptionType"),
                from_address=item.get("fromAddress"),
                use_default_credentials=item.get("useDefaultCredentials"),
                username=item.get("username")
            )
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            smtp_setting = self.get_smtp_settings_by_id(smtp_settings_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return smtp_setting

    def update_smtp_settings(self, smtp_settings_id, password, host, port, encryption_type, from_address,
                             use_default_credentials, username):
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
            Boolean
        """
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

        url = config.get("base_url") + "/cxrestapi/auth/SMTPSettings/{id}".format(id=smtp_settings_id)
        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_smtp_settings(smtp_settings_id, password, host, port, encryption_type,
                                                      from_address,
                                                      use_default_credentials, username)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_smtp_settings(self, smtp_settings_id):
        """

        Args:
            smtp_settings_id (int):

        Returns:
            Boolean
        """

        url = config.get("base_url") + "/cxrestapi/auth/SMTPSettings/{id}".format(id=smtp_settings_id)
        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_smtp_settings(smtp_settings_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def test_smtp_connection(self, receiver_email, password, host, port, encryption_type, from_address,
                             use_default_credentials, username):
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
            Boolean
        """
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

        url = config.get("base_url") + "/cxrestapi/auth/SMTPSettings/testconnection"
        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.test_smtp_connection(receiver_email, password, host, port, encryption_type,
                                                      from_address,
                                                      use_default_credentials, username)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_all_system_locales(self):
        """

        Returns:
            list[SystemLocale]
        """
        url = config.get("base_url") + "/cxrestapi/auth/SystemLocales"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            all_system_locales = [
                SystemLocale(
                    system_locale_id=item.get("id"),
                    lcid=item.get("lcid"),
                    code=item.get("code"),
                    display_name=item.get("displayName")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            all_system_locales = self.get_all_system_locales()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_system_locales

    def get_members_by_team_id(self, team_id):
        """

        Args:
            team_id (int):

        Returns:
            list[User]
        """
        url = config.get("base_url") + "/cxrestapi/auth/Teams/{id}/Users".format(id=team_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            team_members = [
                User(
                    user_id=item.get("id"),
                    username=item.get("userName"),
                    last_login_date=item.get("lastLoginDate"),
                    role_ids=item.get("roleIds"),
                    team_ids=item.get("teamIds"),
                    authentication_provider_id=item.get("authenticationProviderId"),
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
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            team_members = self.get_members_by_team_id(team_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return team_members

    def update_members_by_team_id(self, team_id, user_ids):
        """

        Args:
            team_id (int):
            user_ids (list[int]):

        Returns:
            bool
        """
        put_data = json.dumps(
            {"userIds": user_ids}
        )

        url = config.get("base_url") + "/cxrestapi/auth/Teams/{teamId}/Users".format(teamId=team_id)
        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_members_by_team_id(team_id, user_ids)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def add_a_user_to_a_team(self, team_id, user_id):
        """

        Args:
            team_id (int):
            user_id (int):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/Teams/{teamId}/Users/{userId}".format(
            teamId=team_id, userId=user_id
        )

        r = requests.post(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.add_a_user_to_a_team(team_id, user_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_a_member_from_a_team(self, team_id, user_id):
        """

        Args:
            team_id (int):
            user_id (int):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/Teams/{teamId}/Users/{userId}".format(teamId=team_id,
                                                                                              userId=user_id)
        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_a_member_from_a_team(team_id, user_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_all_teams(self):
        """

        Returns:
            list[`Team`]
        """
        url = config.get("base_url") + "/cxrestapi/auth/Teams"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            all_teams = [
                Team(
                    team_id=item.get("id"),
                    name=item.get("name"),
                    full_name=item.get("fullName"),
                    parent_id=item.get("parentId")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            all_teams = self.get_all_teams()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_teams

    def get_team_id_by_full_name(self, full_name):
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

    def create_new_team(self, name, parent_id):
        """

        Args:
            name (str):
            parent_id (int):

        Returns:
            bool
        """
        post_data = json.dumps(
            {
                "name": name,
                "parentId": parent_id
            }
        )

        url = config.get("base_url") + "/cxrestapi/auth/Teams"
        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.create_new_team(name, parent_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_team_by_id(self, team_id):
        """

        Args:
            team_id(int):

        Returns:
            Team
        """

        url = config.get("base_url") + "/cxrestapi/auth/Teams/{id}".format(id=team_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            team = Team(
                team_id=item.get("id"),
                name=item.get("name"),
                full_name=item.get("fullName"),
                parent_id=item.get("parentId")
            )
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            team = self.get_team_by_id(team_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return team

    def update_a_team(self, team_id, name, parent_id):
        """

        Args:
            team_id (int):
            name (str):
            parent_id (int):

        Returns:
            bool
        """
        put_data = json.dumps(
            {
                "name": name,
                "parentId": parent_id
            }
        )

        url = config.get("base_url") + "/cxrestapi/auth/Teams/{id}".format(id=team_id)
        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_a_team(team_id, name, parent_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_a_team(self, team_id):
        """

        Args:
            team_id (int):

        Returns:
            bool
        """

        url = config.get("base_url") + "/cxrestapi/auth/Teams/{id}".format(id=team_id)
        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_a_team(team_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def generate_a_new_token_signing_certificate(self):
        """

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/TokenSigningCertificateGeneration"

        r = requests.post(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.generate_a_new_token_signing_certificate()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def upload_a_new_token_signing_certificate(self, certificate_file_path, certificate_password):
        """

        Args:
            certificate_file_path (str):
            certificate_password (str):

        Returns:
            bool
        """
        url = config.get("base_url") + "/cxrestapi/auth/TokenSigningCertificate"

        headers = copy(authHeaders.auth_headers)

        file_name = os.path.basename(certificate_file_path)
        m = MultipartEncoder(
            fields={
                "CertificateFile": (file_name, open(certificate_file_path, 'rb'), "application/zip"),
                "CertificatePassword": str(certificate_password)
            }
        )
        headers.update({"Content-Type": m.content_type})

        r = requests.post(url=url, headers=headers, data=m, verify=config.get("verify"))

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.upload_a_new_token_signing_certificate(certificate_file_path, certificate_password)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_all_users(self):
        """

        Returns:
            list[User]
        """

        url = config.get("base_url") + "/cxrestapi/auth/Users"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            all_users = [
                User(
                    user_id=item.get("id"),
                    username=item.get("userName"),
                    last_login_date=item.get("lastLoginDate"),
                    role_ids=item.get("roleIds"),
                    team_ids=item.get("teamIds"),
                    authentication_provider_id=item.get("authenticationProviderId"),
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
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            all_users = self.get_all_users()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_users

    def get_user_id_by_name(self, username):
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

    def create_new_user(self, username, password, role_ids, team_ids, authentication_provider_id, first_name,
                        last_name, email, phone_number, cell_phone_number, job_title, other, country, active,
                        expiration_date, allowed_ip_list, locale_id):
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

        url = config.get("base_url") + "/cxrestapi/auth/Users"
        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.create_new_user(
                username, password, role_ids, team_ids, authentication_provider_id, first_name,
                last_name, email, phone_number, cell_phone_number, job_title, other, country, active,
                expiration_date, allowed_ip_list, locale_id
            )
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_user_by_id(self, user_id):
        """

        Args:
            user_id (int):

        Returns:
            User
        """
        url = config.get("base_url") + "/cxrestapi/auth/Users/{id}".format(id=user_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            user = User(
                user_id=item.get("id"),
                username=item.get("userName"),
                last_login_date=item.get("lastLoginDate"),
                role_ids=item.get("roleIds"),
                team_ids=item.get("teamIds"),
                authentication_provider_id=item.get("authenticationProviderId"),
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
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            user = self.get_user_by_id(user_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return user

    def update_a_user(self, user_id, role_ids, team_ids, first_name, last_name, email, phone_number, cell_phone_number,
                      job_title, other, country, active, expiration_date, allowed_ip_list, locale_id):
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

        url = config.get("base_url") + "/cxrestapi/auth/Users/{id}".format(id=user_id)
        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_a_user(
                user_id, role_ids, team_ids, first_name, last_name, email, phone_number, cell_phone_number,
                job_title, other, country, active, expiration_date, allowed_ip_list, locale_id
            )
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_a_user(self, user_id):
        """

        Args:
            user_id (int):

        Returns:
            bool
        """

        url = config.get("base_url") + "/cxrestapi/auth/Users/{id}".format(id=user_id)
        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_a_user(user_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def migrate_existing_user(self, creation_date, username, password, role_ids, team_ids, authentication_provider_id,
                              first_name, last_name, email, phone_number, cell_phone_number, job_title, other, country,
                              active, expiration_date, allowed_ip_list, locale_id):

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

        url = config.get("base_url") + "/cxrestapi/auth/Users/migration"
        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.migrate_existing_user(
                creation_date, username, password, role_ids, team_ids, authentication_provider_id,
                first_name, last_name, email, phone_number, cell_phone_number, job_title, other, country,
                active, expiration_date, allowed_ip_list, locale_id
            )
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_all_windows_domains(self):
        """

        Returns:
            list[WindowsDomain]
        """

        url = config.get("base_url") + "/cxrestapi/auth/WindowsDomains"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            all_windows_domains = [
                WindowsDomain(
                    windows_domain_id=item.get("id"),
                    name=item.get("name"),
                    full_qualified_name=item.get("fullyQualifiedName")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            all_windows_domains = self.get_all_windows_domains()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_windows_domains

    def get_windows_domain_id_by_name(self, name):
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

    def create_a_new_windows_domain(self, name, full_qualified_name):
        """

        Args:
            name (str):
            full_qualified_name (str):

        Returns:
            bool
        """
        post_data = json.dumps(
            {
                "name": name,
                "FullyQualifiedName": full_qualified_name
            }
        )

        url = config.get("base_url") + "/cxrestapi/auth/WindowsDomains"
        r = requests.post(
            url=url,
            data=post_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.create_a_new_windows_domain(name, full_qualified_name)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_windows_domain_by_id(self, windows_domain_id):
        """

        Args:
            windows_domain_id (int):

        Returns:
            WindowsDomain
        """
        url = config.get("base_url") + "/cxrestapi/auth/WindowsDomains/{id}".format(id=windows_domain_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            windows_domain = WindowsDomain(
                windows_domain_id=item.get("id"),
                name=item.get("name"),
                full_qualified_name=item.get("fullyQualifiedName")
            )
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            windows_domain = self.get_windows_domain_by_id(windows_domain_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return windows_domain

    def update_a_windows_domain(self, windows_domain_id, name, full_qualified_name):
        """

        Args:
            windows_domain_id (int):
            name (str):
            full_qualified_name (str):

        Returns:
            bool
        """
        put_data = json.dumps(
            {
                "name": name,
                "fullyQualifiedName": full_qualified_name
            }
        )

        url = config.get("base_url") + "/cxrestapi/auth/WindowsDomains/{id}".format(id=windows_domain_id)
        r = requests.put(
            url=url,
            data=put_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_a_windows_domain(windows_domain_id, name, full_qualified_name)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_a_windows_domain(self, windows_domain_id):
        """

        Args:
            windows_domain_id (int):

        Returns:
            bool
        """

        url = config.get("base_url") + "/cxrestapi/auth/WindowsDomains/{id}".format(id=windows_domain_id)
        r = requests.delete(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_a_windows_domain(windows_domain_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_windows_domain_user_entries_by_search_criteria(self, windows_domain_id, contains_pattern=None):
        """

        Args:
            windows_domain_id (int):
            contains_pattern (str):

        Returns:
            list[User]
        """

        url = config.get("base_url") + "/cxrestapi/auth/WindowsDomains/{id}/UserEntries".format(id=windows_domain_id)
        if contains_pattern:
            url += "?containsPattern={}".format(contains_pattern)

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_list = r.json()
            users = [
                User(
                    username=item.get("username"),
                    first_name=item.get("firstname"),
                    last_name=item.get("lastname"),
                    email=item.get("email")
                ) for item in a_list
            ]
        elif r.status_code == FORBIDDEN:
            raise CxError("Forbidden to access", r.status_code)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            users = self.get_windows_domain_user_entries_by_search_criteria(windows_domain_id, contains_pattern)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return users
