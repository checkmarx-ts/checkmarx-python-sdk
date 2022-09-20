class LDAPGroupAndRoleMappingDetail(object):
    def __init__(self, role_id, ldap_group_dn, ldap_group_display_name):
        """

        Args:
            role_id (int):
            ldap_group_dn (str):
            ldap_group_display_name (str):
        """
        self.role_id = role_id
        self.ldap_group_dn = ldap_group_dn
        self.ldap_group_display_name = ldap_group_display_name

    def get_dict(self):
        return {
            "roleId": self.role_id,
            "ldapGroupDn": self.ldap_group_dn,
            "ldapGroupDisplayName": self.ldap_group_display_name
      }

    def __str__(self):
        return """LDAPGroupAndRoleMappingDetail(role_id={}, ldap_group_dn={}, ldap_group_display_name={})""".format(
            self.role_id, self.ldap_group_dn, self.ldap_group_display_name
        )
