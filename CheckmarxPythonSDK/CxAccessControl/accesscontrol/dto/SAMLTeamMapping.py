class SAMLTeamMapping(object):

    def __init__(self, saml_team_mapping_id, saml_identity_provider_id, team_id, team_full_path, saml_attribute_value):
        """

        Args:
            saml_team_mapping_id (int):
            saml_identity_provider_id (int):
            team_id (int):
            team_full_path (str):
            saml_attribute_value (str):
        """
        self.id = saml_team_mapping_id
        self.saml_identity_provider_id = saml_identity_provider_id
        self.team_id = team_id
        self.team_full_path = team_full_path
        self.saml_attribute_value = saml_attribute_value

    def __str__(self):
        return """SAMLTeamMapping(id={}, saml_identity_provider_id={}, team_id={}, team_full_path={}, 
        saml_attribute_value={})""".format(self.id, self.saml_identity_provider_id, self.team_id, self.team_full_path,
                                           self.saml_attribute_value)
