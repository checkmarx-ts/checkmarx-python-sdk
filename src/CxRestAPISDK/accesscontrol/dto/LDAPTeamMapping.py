# encoding: utf-8


class LDAPTeamMapping(object):

    def __init__(self, ldap_team_mapping_id=None, ldap_server_id=None, team_id=None, ldap_group_dn=None,
                 ldap_group_display_name=None):
        """

        Args:
            ldap_team_mapping_id (int):
            ldap_server_id (int):
            team_id (int):
            ldap_group_dn (str):
            ldap_group_display_name (str):
        """
        self.id = ldap_team_mapping_id
        self.ldap_server_id = ldap_server_id
        self.team_id = team_id
        self.ldap_group_dn = ldap_group_dn
        self.ldap_group_display_name = ldap_group_display_name

    def __str__(self):
        return """LDAPTeamMapping(id={}, ldap_server_id={}, team_id={}, ldap_group_dn={}, 
        ldap_group_display_name={})""".format(
            self.id, self.ldap_server_id, self.team_id, self.ldap_group_dn, self.ldap_group_display_name
        )
