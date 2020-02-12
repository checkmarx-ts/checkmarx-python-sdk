# encoding: utf-8


class LDAPRoleMapping(object):
    def __init__(self, ldap_role_mapping_id, ldap_server_id, role_id, ldap_group_dn, ldap_group_display_name):
        """

        Args:
            ldap_role_mapping_id (int):
            ldap_server_id (int):
            role_id (int):
            ldap_group_dn (str):
            ldap_group_display_name (str):
        """
        self.id = ldap_role_mapping_id,
        self.ldap_server_id = ldap_server_id,
        self.role_id = role_id,
        self.ldap_group_dn = ldap_group_dn,
        self.ldap_group_display_name = ldap_group_display_name

    def __str__(self):
        return """LDAPRoleMapping(id={}, ldap_server_id={}, role_id={}, ldap_group_dn={}, 
        ldap_group_display_name={})""".format(
            self.id, self.ldap_server_id, self.role_id, self.ldap_group_dn, self.ldap_group_display_name
        )
