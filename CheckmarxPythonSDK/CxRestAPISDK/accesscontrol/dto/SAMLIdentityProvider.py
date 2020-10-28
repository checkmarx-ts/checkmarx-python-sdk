# encoding: utf-8


class SAMLIdentityProvider(object):

    def __init__(self, saml_identity_provider_id, certificate_file_name, certificate_subject, active, name, issuer,
                 login_url, logout_url, error_url, sign_authn_request, authn_request_binding, is_manual_management,
                 default_team_id, default_role_id):
        """

        Args:
            saml_identity_provider_id (int):
            certificate_file_name (str):
            certificate_subject (str):
            active (bool):
            name (str):
            issuer (str):
            login_url (str):
            logout_url (str):
            error_url (str):
            sign_authn_request (bool):
            authn_request_binding (str):
            is_manual_management (bool):
            default_team_id (int, None):
            default_role_id (int, None):
        """
        self.id = saml_identity_provider_id
        self.certificate_file_name = certificate_file_name
        self.certificate_subject = certificate_subject
        self.active = active
        self.name = name
        self.issuer = issuer
        self.login_url = login_url
        self.logout_url = logout_url
        self.error_url = error_url
        self.sign_authn_request = sign_authn_request
        self.authn_request_binding = authn_request_binding
        self.is_manual_management = is_manual_management
        self.default_team_id = default_team_id
        self.default_role_id = default_role_id

    def __str__(self):
        return """SAMLIdentityProvider(id={}, certificate_file_name={}, certificate_subject={}, active={}, name={}, 
        issuer={}, login_url={}, logout_url={}, error_url={}, sign_authn_request={}, authn_request_binding={}, 
        is_manual_management={}, default_team_id={}, default_role_id={})""".format(
            self.id, self.certificate_file_name, self.certificate_subject, self.active, self.name, self.issuer,
            self.login_url, self.logout_url, self.error_url, self.sign_authn_request, self.authn_request_binding,
            self.is_manual_management, self.default_team_id, self.default_role_id
        )
