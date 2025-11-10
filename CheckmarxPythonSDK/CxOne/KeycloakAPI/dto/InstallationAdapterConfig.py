from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .PolicyEnforcerConfig import PolicyEnforcerConfig


@dataclass
class InstallationAdapterConfig:
    realm: Optional[str] = None
    realm_public_key: Optional[str] = None
    auth_server_url: Optional[str] = None
    ssl_required: Optional[str] = None
    bearer_only: Optional[bool] = None
    resource: Optional[str] = None
    public_client: Optional[bool] = None
    verify_token_audience: Optional[bool] = None
    credentials: Optional[Dict[str, Any]] = None
    use_resource_role_mappings: Optional[bool] = None
    confidential_port: Optional[int] = None
    policy_enforcer: Optional[PolicyEnforcerConfig] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.realm is not None:
            value = self.realm
            result['realm'] = value
        if self.realm_public_key is not None:
            value = self.realm_public_key
            result['realmPublicKey'] = value
        if self.auth_server_url is not None:
            value = self.auth_server_url
            result['authServerUrl'] = value
        if self.ssl_required is not None:
            value = self.ssl_required
            result['sslRequired'] = value
        if self.bearer_only is not None:
            value = self.bearer_only
            result['bearerOnly'] = value
        if self.resource is not None:
            value = self.resource
            result['resource'] = value
        if self.public_client is not None:
            value = self.public_client
            result['publicClient'] = value
        if self.verify_token_audience is not None:
            value = self.verify_token_audience
            result['verifyTokenAudience'] = value
        if self.credentials is not None:
            value = self.credentials
            result['credentials'] = value
        if self.use_resource_role_mappings is not None:
            value = self.use_resource_role_mappings
            result['useResourceRoleMappings'] = value
        if self.confidential_port is not None:
            value = self.confidential_port
            result['confidentialPort'] = value
        if self.policy_enforcer is not None:
            value = self.policy_enforcer.to_dict()
            result['policyEnforcer'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'policy_enforcer' in snake_data and snake_data['policy_enforcer'] is not None:
            snake_data['policy_enforcer'] = PolicyEnforcerConfig.from_dict(snake_data['policy_enforcer'])
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
