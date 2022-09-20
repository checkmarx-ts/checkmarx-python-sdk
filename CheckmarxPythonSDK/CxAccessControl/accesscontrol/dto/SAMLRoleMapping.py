# encoding: utf-8


class SAMLRoleMapping(object):

    def __init__(self, saml_role_mapping_id, saml_identity_provider_id, role_id, role_name, saml_attribute_value):
        """

        Args:
            saml_role_mapping_id (int):
            saml_identity_provider_id (int):
            role_id (int):
            role_name (str):
            saml_attribute_value (str):
        """
        self.id = saml_role_mapping_id
        self.saml_identity_provider_id = saml_identity_provider_id
        self.role_id = role_id
        self.role_name = role_name
        self.saml_attribute_value = saml_attribute_value

    def __str__(self):
        return """SAMLRoleMapping(id={}, saml_identity_provider_id={}, role_id={}, role_name={}, 
        saml_attribute_value={})""".format(self.id, self.saml_identity_provider_id, self.role_id, self.role_name,
                                           self.saml_attribute_value)
