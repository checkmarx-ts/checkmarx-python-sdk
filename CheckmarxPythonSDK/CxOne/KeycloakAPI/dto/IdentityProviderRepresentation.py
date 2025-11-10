from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class IdentityProviderRepresentation:
    alias: Optional[str] = None
    display_name: Optional[str] = None
    internal_id: Optional[str] = None
    provider_id: Optional[str] = None
    enabled: Optional[bool] = None
    update_profile_first_login_mode: Optional[str] = None
    trust_email: Optional[bool] = None
    store_token: Optional[bool] = None
    add_read_token_role_on_create: Optional[bool] = None
    authenticate_by_default: Optional[bool] = None
    link_only: Optional[bool] = None
    first_broker_login_flow_alias: Optional[str] = None
    post_broker_login_flow_alias: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    update_profile_first_login: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.alias is not None:
            value = self.alias
            result['alias'] = value
        if self.display_name is not None:
            value = self.display_name
            result['displayName'] = value
        if self.internal_id is not None:
            value = self.internal_id
            result['internalId'] = value
        if self.provider_id is not None:
            value = self.provider_id
            result['providerId'] = value
        if self.enabled is not None:
            value = self.enabled
            result['enabled'] = value
        if self.update_profile_first_login_mode is not None:
            value = self.update_profile_first_login_mode
            result['updateProfileFirstLoginMode'] = value
        if self.trust_email is not None:
            value = self.trust_email
            result['trustEmail'] = value
        if self.store_token is not None:
            value = self.store_token
            result['storeToken'] = value
        if self.add_read_token_role_on_create is not None:
            value = self.add_read_token_role_on_create
            result['addReadTokenRoleOnCreate'] = value
        if self.authenticate_by_default is not None:
            value = self.authenticate_by_default
            result['authenticateByDefault'] = value
        if self.link_only is not None:
            value = self.link_only
            result['linkOnly'] = value
        if self.first_broker_login_flow_alias is not None:
            value = self.first_broker_login_flow_alias
            result['firstBrokerLoginFlowAlias'] = value
        if self.post_broker_login_flow_alias is not None:
            value = self.post_broker_login_flow_alias
            result['postBrokerLoginFlowAlias'] = value
        if self.config is not None:
            value = self.config
            result['config'] = value
        if self.update_profile_first_login is not None:
            value = self.update_profile_first_login
            result['updateProfileFirstLogin'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
