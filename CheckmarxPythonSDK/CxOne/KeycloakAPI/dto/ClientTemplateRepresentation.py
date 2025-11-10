from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ProtocolMapperRepresentation import ProtocolMapperRepresentation


@dataclass
class ClientTemplateRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    protocol: Optional[str] = None
    full_scope_allowed: Optional[bool] = None
    bearer_only: Optional[bool] = None
    consent_required: Optional[bool] = None
    standard_flow_enabled: Optional[bool] = None
    implicit_flow_enabled: Optional[bool] = None
    direct_access_grants_enabled: Optional[bool] = None
    service_accounts_enabled: Optional[bool] = None
    public_client: Optional[bool] = None
    frontchannel_logout: Optional[bool] = None
    attributes: Optional[Dict[str, Any]] = None
    protocol_mappers: Optional[List[ProtocolMapperRepresentation]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.description is not None:
            value = self.description
            result['description'] = value
        if self.protocol is not None:
            value = self.protocol
            result['protocol'] = value
        if self.full_scope_allowed is not None:
            value = self.full_scope_allowed
            result['fullScopeAllowed'] = value
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
        if self.public_client is not None:
            value = self.public_client
            result['publicClient'] = value
        if self.frontchannel_logout is not None:
            value = self.frontchannel_logout
            result['frontchannelLogout'] = value
        if self.attributes is not None:
            value = self.attributes
            result['attributes'] = value
        if self.protocol_mappers is not None:
            value = [item.to_dict() for item in self.protocol_mappers]
            result['protocolMappers'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'protocol_mappers' in snake_data and snake_data['protocol_mappers'] is not None:
            snake_data['protocol_mappers'] = [
                ProtocolMapperRepresentation.from_dict(item) for item in snake_data['protocol_mappers']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
