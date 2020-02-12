# encoding: utf-8


class LDAPServer(object):

    def __init__(self, ldap_server_id, active, name, host, port, username, use_ssl, verify_ssl_certificate,
                 ldap_directory_type, sso_enabled, mapped_domain_id, based_dn, additional_user_dn, user_object_filter,
                 user_object_class, username_attribute, first_name_attribute, last_name_attribute, email_attribute,
                 synchronization_enabled, default_team_id, default_role_id, update_team_and_role_upon_login_enabled,
                 periodical_synchronization_enabled, advanced_team_and_role_mapping_enabled, additional_group_dn,
                 group_object_class, group_object_filter, group_name_attribute, group_members_attribute,
                 user_membership_attribute):
        """

        Args:
            ldap_server_id (int):
            active (bool) :
            name (str):
            host (str):
            port (int):
            username (str):
            use_ssl (bool):
            verify_ssl_certificate (bool):
            ldap_directory_type (str):
            sso_enabled (bool):
            mapped_domain_id (int):
            based_dn (str):
            additional_user_dn (str):
            user_object_filter (str):
            user_object_class (str):
            username_attribute (str):
            first_name_attribute (str):
            last_name_attribute (str):
            email_attribute (str):
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
        """
        self.id = ldap_server_id
        self.active = active
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self.use_ssl = use_ssl
        self.verify_ssl_certificate = verify_ssl_certificate
        self.ldap_directory_type = ldap_directory_type
        self.sso_enabled = sso_enabled
        self.mapped_domain_id = mapped_domain_id
        self.based_dn = based_dn
        self.additional_user_dn = additional_user_dn
        self.user_object_filter = user_object_filter
        self.user_object_class = user_object_class
        self.username_attribute = username_attribute
        self.first_name_attribute = first_name_attribute
        self.last_name_attribute = last_name_attribute
        self.email_attribute = email_attribute
        self.synchronization_enabled = synchronization_enabled
        self.default_team_id = default_team_id
        self.default_role_id = default_role_id
        self.update_team_and_role_upon_login_enabled = update_team_and_role_upon_login_enabled
        self.periodical_synchronization_enabled = periodical_synchronization_enabled
        self.advanced_team_and_role_mapping_enabled = advanced_team_and_role_mapping_enabled
        self.additional_group_dn = additional_group_dn
        self.group_object_class = group_object_class
        self.group_object_filter = group_object_filter
        self.group_name_attribute = group_name_attribute
        self.group_members_attribute = group_members_attribute
        self.user_membership_attribute = user_membership_attribute

    def __str__(self):
        return """LDAPServer(id={}, active={}, name={}, host={}, port={}, username={}, use_ssl={}, 
        verify_ssl_certificate={}, ldap_directory_type={}, sso_enabled={}, mapped_domain_id={}, based_dn={}, 
        additional_user_dn={}, user_object_filter={}, user_object_class={}, username_attribute={}, 
        first_name_attribute={}, last_name_attribute={}, email_attribute={}, synchronization_enabled={}, 
        default_team_id={}, default_role_id={}, update_team_and_role_upon_login_enabled={},
        periodical_synchronization_enabled={}, advanced_team_and_role_mapping_enabled={}, additional_group_dn={},
        group_object_class={}, group_object_filter={}, group_name_attribute={}, group_members_attribute={}, 
        user_membership_attribute={})""".format(
            self.id, self.active, self.name, self.host, self.port, self.username, self.use_ssl,
            self.verify_ssl_certificate, self.ldap_directory_type, self.sso_enabled, self.mapped_domain_id,
            self.based_dn, self.additional_user_dn, self.user_object_filter,
            self.user_object_class, self.username_attribute, self.first_name_attribute, self.last_name_attribute,
            self.email_attribute, self.synchronization_enabled, self.default_team_id, self.default_role_id,
            self.update_team_and_role_upon_login_enabled, self.periodical_synchronization_enabled,
            self.advanced_team_and_role_mapping_enabled, self.additional_group_dn,
            self.group_object_class, self.group_object_filter, self.group_name_attribute, self.group_members_attribute,
            self.user_membership_attribute
        )
