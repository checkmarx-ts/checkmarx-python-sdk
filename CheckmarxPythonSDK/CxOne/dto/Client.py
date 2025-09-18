from dataclasses import dataclass
from typing import List
from .ProtocolMappersRepresentation import ProtocolMappersRepresentation, construct_protocol_mappers_representation


@dataclass
class Client:
    id: str = None
    client_id: str = None
    root_url: str = None
    admin_url: str = None
    surrogate_auth_required: bool = None
    enabled: bool = None
    always_display_in_console: bool = None
    client_authenticator_type: str = None
    redirect_uris: List[str] = None
    not_before: int = None
    bearer_only: bool = None
    consent_required: bool = None
    standard_flow_enabled: bool = None
    implicit_flow_enabled: bool = None
    direct_access_grants_enabled: bool = None
    service_accounts_enabled: bool = None
    public_client: bool = None
    front_channel_logout: bool = None
    protocol: str = None
    attributes: dict = None
    authentication_flow_binding_overrides: dict = None
    full_scope_allowed: bool = None
    node_re_registration_timeout: int = None
    protocol_mappers: List[ProtocolMappersRepresentation] = None
    default_client_scopes: List[str] = None


def construct_client(item):
    return Client(
        id=item.get("id"),
        client_id=item.get("clientId"),
        root_url=item.get("rootUrl"),
        admin_url=item.get("adminUrl"),
        surrogate_auth_required=item.get("surrogateAuthRequired"),
        enabled=item.get("enabled"),
        always_display_in_console=item.get("alwaysDisplayInConsole"),
        client_authenticator_type=item.get("clientAuthenticatorType"),
        redirect_uris=item.get("redirectUris"),
        not_before=item.get("notBefore"),
        bearer_only=item.get("bearerOnly"),
        consent_required=item.get("consentRequired"),
        standard_flow_enabled=item.get("standardFlowEnabled"),
        implicit_flow_enabled=item.get("implicitFlowEnabled"),
        direct_access_grants_enabled=item.get("directAccessGrantsEnabled"),
        service_accounts_enabled=item.get("serviceAccountsEnabled"),
        public_client=item.get("publicClient"),
        front_channel_logout=item.get("frontchannelLogout"),
        protocol=item.get("protocol"),
        attributes=item.get("attributes"),
        authentication_flow_binding_overrides=item.get("authenticationFlowBindingOverrides"),
        full_scope_allowed=item.get("fullScopeAllowed"),
        node_re_registration_timeout=item.get("nodeReRegistrationTimeout"),
        protocol_mappers=[
            construct_protocol_mappers_representation(mapper) for mapper in item.get("protocolMappers", [])
        ],
        default_client_scopes=item.get("defaultClientScopes"),
    )
