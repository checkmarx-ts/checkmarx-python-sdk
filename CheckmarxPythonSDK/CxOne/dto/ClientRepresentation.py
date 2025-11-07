class ClientRepresentation:
    def __init__(self, access, admin_url, always_display_in_console, attributes, authentication_flow_binding_overrides,
                 authorization_services_enabled, authorization_settings, base_url, bearer_only,
                 client_authenticator_type, client_id, consent_required, default_client_scopes, description,
                 direct_access_grants_enabled, enabled, frontchannel_logout, full_scope_allowed,
                 client_representation_id, implicit_flow_enabled, name, node_re_registration_timeout, not_before,
                 oauth2_device_authorization_grant_enabled, optional_client_scopes, origin, protocol, protocol_mappers,
                 public_client, redirect_uris, registered_nodes, registration_access_token, root_url, secret,
                 service_accounts_enabled, standard_flow_enabled, surrogate_auth_required, web_origins):
        self.access = access
        self.adminUrl = admin_url
        self.alwaysDisplayInConsole = always_display_in_console
        self.attributes = attributes
        self.authenticationFlowBindingOverrides = authentication_flow_binding_overrides
        self.authorizationServicesEnabled = authorization_services_enabled
        self.authorizationSettings = authorization_settings
        self.baseUrl = base_url
        self.bearerOnly = bearer_only
        self.clientAuthenticatorType = client_authenticator_type
        self.clientId = client_id
        self.consentRequired = consent_required
        self.defaultClientScopes = default_client_scopes
        self.description = description
        self.directAccessGrantsEnabled = direct_access_grants_enabled
        self.enabled = enabled
        self.frontchannelLogout = frontchannel_logout
        self.fullScopeAllowed = full_scope_allowed
        self.id = client_representation_id
        self.implicitFlowEnabled = implicit_flow_enabled
        self.name = name
        self.nodeReRegistrationTimeout = node_re_registration_timeout
        self.notBefore = not_before
        self.oauth2DeviceAuthorizationGrantEnabled = oauth2_device_authorization_grant_enabled
        self.optionalClientScopes = optional_client_scopes
        self.origin = origin
        self.protocol = protocol
        self.protocolMappers = protocol_mappers
        self.publicClient = public_client
        self.redirectUris = redirect_uris
        self.registeredNodes = registered_nodes
        self.registrationAccessToken = registration_access_token
        self.rootUrl = root_url
        self.secret = secret
        self.serviceAccountsEnabled = service_accounts_enabled
        self.standardFlowEnabled = standard_flow_enabled
        self.surrogateAuthRequired = surrogate_auth_required
        self.webOrigins = web_origins

    def __str__(self):
        return f"ClientRepresentation(" \
               f"access={self.access} " \
               f"adminUrl={self.adminUrl} " \
               f"alwaysDisplayInConsole={self.alwaysDisplayInConsole} " \
               f"attributes={self.attributes} " \
               f"authenticationFlowBindingOverrides={self.authenticationFlowBindingOverrides} " \
               f"authorizationServicesEnabled={self.authorizationServicesEnabled} " \
               f"authorizationSettings={self.authorizationSettings} " \
               f"baseUrl={self.baseUrl} " \
               f"bearerOnly={self.bearerOnly} " \
               f"clientAuthenticatorType={self.clientAuthenticatorType} " \
               f"clientId={self.clientId} " \
               f"consentRequired={self.consentRequired} " \
               f"defaultClientScopes={self.defaultClientScopes} " \
               f"description={self.description} " \
               f"directAccessGrantsEnabled={self.directAccessGrantsEnabled} " \
               f"enabled={self.enabled} " \
               f"frontchannelLogout={self.frontchannelLogout} " \
               f"fullScopeAllowed={self.fullScopeAllowed} " \
               f"id={self.id} " \
               f"implicitFlowEnabled={self.implicitFlowEnabled} " \
               f"name={self.name} " \
               f"nodeReRegistrationTimeout={self.nodeReRegistrationTimeout} " \
               f"notBefore={self.notBefore} " \
               f"oauth2DeviceAuthorizationGrantEnabled={self.oauth2DeviceAuthorizationGrantEnabled} " \
               f"optionalClientScopes={self.optionalClientScopes} " \
               f"origin={self.origin} " \
               f"protocol={self.protocol} " \
               f"protocolMappers={self.protocolMappers} " \
               f"publicClient={self.publicClient} " \
               f"redirectUris={self.redirectUris} " \
               f"registeredNodes={self.registeredNodes} " \
               f"registrationAccessToken={self.registrationAccessToken} " \
               f"rootUrl={self.rootUrl} " \
               f"secret={self.secret} " \
               f"serviceAccountsEnabled={self.serviceAccountsEnabled} " \
               f"standardFlowEnabled={self.standardFlowEnabled} " \
               f"surrogateAuthRequired={self.surrogateAuthRequired} " \
               f"webOrigins={self.webOrigins} " \
               f")"

    def to_dict(self):
        return {
            "access": self.access,
            "adminUrl": self.adminUrl,
            "alwaysDisplayInConsole": self.alwaysDisplayInConsole,
            "attributes": self.attributes,
            "authenticationFlowBindingOverrides": self.authenticationFlowBindingOverrides,
            "authorizationServicesEnabled": self.authorizationServicesEnabled,
            "authorizationSettings": self.authorizationSettings,
            "baseUrl": self.baseUrl,
            "bearerOnly": self.bearerOnly,
            "clientAuthenticatorType": self.clientAuthenticatorType,
            "clientId": self.clientId,
            "consentRequired": self.consentRequired,
            "defaultClientScopes": self.defaultClientScopes,
            "description": self.description,
            "directAccessGrantsEnabled": self.directAccessGrantsEnabled,
            "enabled": self.enabled,
            "frontchannelLogout": self.frontchannelLogout,
            "fullScopeAllowed": self.fullScopeAllowed,
            "id": self.id,
            "implicitFlowEnabled": self.implicitFlowEnabled,
            "name": self.name,
            "nodeReRegistrationTimeout": self.nodeReRegistrationTimeout,
            "notBefore": self.notBefore,
            "oauth2DeviceAuthorizationGrantEnabled": self.oauth2DeviceAuthorizationGrantEnabled,
            "optionalClientScopes": self.optionalClientScopes,
            "origin": self.origin,
            "protocol": self.protocol,
            "protocolMappers": self.protocolMappers,
            "publicClient": self.publicClient,
            "redirectUris": self.redirectUris,
            "registeredNodes": self.registeredNodes,
            "registrationAccessToken": self.registrationAccessToken,
            "rootUrl": self.rootUrl,
            "secret": self.secret,
            "serviceAccountsEnabled": self.serviceAccountsEnabled,
            "standardFlowEnabled": self.standardFlowEnabled,
            "surrogateAuthRequired": self.surrogateAuthRequired,
            "webOrigins": self.webOrigins,
        }


def construct_client_representation(item):
    return ClientRepresentation(
        access=item.get("access"),
        admin_url=item.get("adminUrl"),
        always_display_in_console=item.get("alwaysDisplayInConsole"),
        attributes=item.get("attributes"),
        authentication_flow_binding_overrides=item.get("authenticationFlowBindingOverrides"),
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
        oauth2_device_authorization_grant_enabled=item.get("oauth2DeviceAuthorizationGrantEnabled"),
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
