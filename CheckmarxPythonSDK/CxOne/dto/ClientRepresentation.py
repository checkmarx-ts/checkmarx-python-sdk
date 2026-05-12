from dataclasses import dataclass


@dataclass
class ClientRepresentation:
    access: ... = None
    admin_url: ... = None
    always_display_in_console: ... = None
    attributes: ... = None
    authentication_flow_binding_overrides: ... = None
    authorization_services_enabled: ... = None
    authorization_settings: ... = None
    base_url: ... = None
    bearer_only: ... = None
    client_authenticator_type: ... = None
    client_id: ... = None
    consent_required: ... = None
    default_client_scopes: ... = None
    description: ... = None
    direct_access_grants_enabled: ... = None
    enabled: ... = None
    frontchannel_logout: ... = None
    full_scope_allowed: ... = None
    client_representation_id: ... = None
    implicit_flow_enabled: ... = None
    name: ... = None
    node_re_registration_timeout: ... = None
    not_before: ... = None
    oauth2_device_authorization_grant_enabled: ... = None
    optional_client_scopes: ... = None
    origin: ... = None
    protocol: ... = None
    protocol_mappers: ... = None
    public_client: ... = None
    redirect_uris: ... = None
    registered_nodes: ... = None
    registration_access_token: ... = None
    root_url: ... = None
    secret: ... = None
    service_accounts_enabled: ... = None
    standard_flow_enabled: ... = None
    surrogate_auth_required: ... = None
    web_origins: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientRepresentation":
        return cls(
            access=item.get("access"),
            admin_url=item.get("adminUrl"),
            always_display_in_console=item.get("alwaysDisplayInConsole"),
            attributes=item.get("attributes"),
            authentication_flow_binding_overrides=item.get(
                "authenticationFlowBindingOverrides"
            ),
            authorization_services_enabled=item.get("authorizationServicesEnabled"),
            authorization_settings=item.get("authorizationSettings"),
            base_url=item.get("baseUrl"),
            bearer_only=item.get("bearerOnly"),
            client_authenticator_type=item.get("clientAuthenticatorType"),
            client_id=item.get("clientId"),
            consent_required=item.get("consentRequired"),
            default_client_scopes=item.get("defaultClientScopes"),
            description=item.get("description"),
            direct_access_grants_enabled=item.get("directAccessGrantsEnabled"),
            enabled=item.get("enabled"),
            frontchannel_logout=item.get("frontchannelLogout"),
            full_scope_allowed=item.get("fullScopeAllowed"),
            client_representation_id=item.get("id"),
            implicit_flow_enabled=item.get("implicitFlowEnabled"),
            name=item.get("name"),
            node_re_registration_timeout=item.get("nodeReRegistrationTimeout"),
            not_before=item.get("notBefore"),
            oauth2_device_authorization_grant_enabled=item.get(
                "oauth2DeviceAuthorizationGrantEnabled"
            ),
            optional_client_scopes=item.get("optionalClientScopes"),
            origin=item.get("origin"),
            protocol=item.get("protocol"),
            protocol_mappers=item.get("protocolMappers"),
            public_client=item.get("publicClient"),
            redirect_uris=item.get("redirectUris"),
            registered_nodes=item.get("registeredNodes"),
            registration_access_token=item.get("registrationAccessToken"),
            root_url=item.get("rootUrl"),
            secret=item.get("secret"),
            service_accounts_enabled=item.get("serviceAccountsEnabled"),
            standard_flow_enabled=item.get("standardFlowEnabled"),
            surrogate_auth_required=item.get("surrogateAuthRequired"),
            web_origins=item.get("webOrigins"),
        )
