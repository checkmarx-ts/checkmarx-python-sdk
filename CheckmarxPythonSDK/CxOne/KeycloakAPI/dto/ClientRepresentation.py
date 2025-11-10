from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ProtocolMapperRepresentation import ProtocolMapperRepresentation
from .ResourceServerRepresentation import ResourceServerRepresentation


@dataclass
class ClientRepresentation:
    id: Optional[str] = None
    client_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    root_url: Optional[str] = None
    admin_url: Optional[str] = None
    base_url: Optional[str] = None
    surrogate_auth_required: Optional[bool] = None
    enabled: Optional[bool] = None
    always_display_in_console: Optional[bool] = None
    client_authenticator_type: Optional[str] = None
    secret: Optional[str] = None
    registration_access_token: Optional[str] = None
    default_roles: Optional[List[str]] = None
    redirect_uris: Optional[List[str]] = None
    web_origins: Optional[List[str]] = None
    not_before: Optional[int] = None
    bearer_only: Optional[bool] = None
    consent_required: Optional[bool] = None
    standard_flow_enabled: Optional[bool] = None
    implicit_flow_enabled: Optional[bool] = None
    direct_access_grants_enabled: Optional[bool] = None
    service_accounts_enabled: Optional[bool] = None
    oauth2_device_authorization_grant_enabled: Optional[bool] = None
    authorization_services_enabled: Optional[bool] = None
    direct_grants_only: Optional[bool] = None
    public_client: Optional[bool] = None
    frontchannel_logout: Optional[bool] = None
    protocol: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    authentication_flow_binding_overrides: Optional[Dict[str, Any]] = None
    full_scope_allowed: Optional[bool] = None
    node_re_registration_timeout: Optional[int] = None
    registered_nodes: Optional[Dict[str, Any]] = None
    protocol_mappers: Optional[List[ProtocolMapperRepresentation]] = None
    client_template: Optional[str] = None
    use_template_config: Optional[bool] = None
    use_template_scope: Optional[bool] = None
    use_template_mappers: Optional[bool] = None
    default_client_scopes: Optional[List[str]] = None
    optional_client_scopes: Optional[List[str]] = None
    authorization_settings: Optional[ResourceServerRepresentation] = None
    access: Optional[Dict[str, Any]] = None
    origin: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.client_id is not None:
            value = self.client_id
            result['clientId'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.description is not None:
            value = self.description
            result['description'] = value
        if self.root_url is not None:
            value = self.root_url
            result['rootUrl'] = value
        if self.admin_url is not None:
            value = self.admin_url
            result['adminUrl'] = value
        if self.base_url is not None:
            value = self.base_url
            result['baseUrl'] = value
        if self.surrogate_auth_required is not None:
            value = self.surrogate_auth_required
            result['surrogateAuthRequired'] = value
        if self.enabled is not None:
            value = self.enabled
            result['enabled'] = value
        if self.always_display_in_console is not None:
            value = self.always_display_in_console
            result['alwaysDisplayInConsole'] = value
        if self.client_authenticator_type is not None:
            value = self.client_authenticator_type
            result['clientAuthenticatorType'] = value
        if self.secret is not None:
            value = self.secret
            result['secret'] = value
        if self.registration_access_token is not None:
            value = self.registration_access_token
            result['registrationAccessToken'] = value
        if self.default_roles is not None:
            value = self.default_roles
            result['defaultRoles'] = value
        if self.redirect_uris is not None:
            value = self.redirect_uris
            result['redirectUris'] = value
        if self.web_origins is not None:
            value = self.web_origins
            result['webOrigins'] = value
        if self.not_before is not None:
            value = self.not_before
            result['notBefore'] = value
        if self.bearer_only is not None:
            value = self.bearer_only
            result['bearerOnly'] = value
        if self.consent_required is not None:
            value = self.consent_required
            result['consentRequired'] = value
        if self.standard_flow_enabled is not None:
            value = self.standard_flow_enabled
            result['standardFlowEnabled'] = value
        if self.implicit_flow_enabled is not None:
            value = self.implicit_flow_enabled
            result['implicitFlowEnabled'] = value
        if self.direct_access_grants_enabled is not None:
            value = self.direct_access_grants_enabled
            result['directAccessGrantsEnabled'] = value
        if self.service_accounts_enabled is not None:
            value = self.service_accounts_enabled
            result['serviceAccountsEnabled'] = value
        if self.oauth2_device_authorization_grant_enabled is not None:
            value = self.oauth2_device_authorization_grant_enabled
            result['oauth2DeviceAuthorizationGrantEnabled'] = value
        if self.authorization_services_enabled is not None:
            value = self.authorization_services_enabled
            result['authorizationServicesEnabled'] = value
        if self.direct_grants_only is not None:
            value = self.direct_grants_only
            result['directGrantsOnly'] = value
        if self.public_client is not None:
            value = self.public_client
            result['publicClient'] = value
        if self.frontchannel_logout is not None:
            value = self.frontchannel_logout
            result['frontchannelLogout'] = value
        if self.protocol is not None:
            value = self.protocol
            result['protocol'] = value
        if self.attributes is not None:
            value = self.attributes
            result['attributes'] = value
        if self.authentication_flow_binding_overrides is not None:
            value = self.authentication_flow_binding_overrides
            result['authenticationFlowBindingOverrides'] = value
        if self.full_scope_allowed is not None:
            value = self.full_scope_allowed
            result['fullScopeAllowed'] = value
        if self.node_re_registration_timeout is not None:
            value = self.node_re_registration_timeout
            result['nodeReRegistrationTimeout'] = value
        if self.registered_nodes is not None:
            value = self.registered_nodes
            result['registeredNodes'] = value
        if self.protocol_mappers is not None:
            value = [item.to_dict() for item in self.protocol_mappers]
            result['protocolMappers'] = value
        if self.client_template is not None:
            value = self.client_template
            result['clientTemplate'] = value
        if self.use_template_config is not None:
            value = self.use_template_config
            result['useTemplateConfig'] = value
        if self.use_template_scope is not None:
            value = self.use_template_scope
            result['useTemplateScope'] = value
        if self.use_template_mappers is not None:
            value = self.use_template_mappers
            result['useTemplateMappers'] = value
        if self.default_client_scopes is not None:
            value = self.default_client_scopes
            result['defaultClientScopes'] = value
        if self.optional_client_scopes is not None:
            value = self.optional_client_scopes
            result['optionalClientScopes'] = value
        if self.authorization_settings is not None:
            value = self.authorization_settings.to_dict()
            result['authorizationSettings'] = value
        if self.access is not None:
            value = self.access
            result['access'] = value
        if self.origin is not None:
            value = self.origin
            result['origin'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'authorization_settings' in snake_data and snake_data['authorization_settings'] is not None:
            snake_data['authorization_settings'] = ResourceServerRepresentation.from_dict(
                snake_data['authorization_settings'])
        if 'protocol_mappers' in snake_data and snake_data['protocol_mappers'] is not None:
            snake_data['protocol_mappers'] = [
                ProtocolMapperRepresentation.from_dict(item) for item in snake_data['protocol_mappers']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
