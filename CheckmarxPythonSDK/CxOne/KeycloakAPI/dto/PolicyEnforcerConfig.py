from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .EnforcementMode import EnforcementMode
from .PathCacheConfig import PathCacheConfig
from .PathConfig import PathConfig


@dataclass
class PolicyEnforcerConfig:
    enforcement_mode: Optional[EnforcementMode] = None
    paths: Optional[List[PathConfig]] = None
    path_cache: Optional[PathCacheConfig] = None
    lazy_load_paths: Optional[bool] = None
    on_deny_redirect_to: Optional[str] = None
    user_managed_access: Optional[Dict[str, Any]] = None
    claim_information_point: Optional[Dict[str, Any]] = None
    http_method_as_scope: Optional[bool] = None
    realm: Optional[str] = None
    auth_server_url: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None
    resource: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.enforcement_mode is not None:
            value = self.enforcement_mode.to_dict()
            result['enforcementMode'] = value
        if self.paths is not None:
            value = [item.to_dict() for item in self.paths]
            result['paths'] = value
        if self.path_cache is not None:
            value = self.path_cache.to_dict()
            result['pathCache'] = value
        if self.lazy_load_paths is not None:
            value = self.lazy_load_paths
            result['lazyLoadPaths'] = value
        if self.on_deny_redirect_to is not None:
            value = self.on_deny_redirect_to
            result['onDenyRedirectTo'] = value
        if self.user_managed_access is not None:
            value = self.user_managed_access
            result['userManagedAccess'] = value
        if self.claim_information_point is not None:
            value = self.claim_information_point
            result['claimInformationPoint'] = value
        if self.http_method_as_scope is not None:
            value = self.http_method_as_scope
            result['httpMethodAsScope'] = value
        if self.realm is not None:
            value = self.realm
            result['realm'] = value
        if self.auth_server_url is not None:
            value = self.auth_server_url
            result['authServerUrl'] = value
        if self.credentials is not None:
            value = self.credentials
            result['credentials'] = value
        if self.resource is not None:
            value = self.resource
            result['resource'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'enforcement_mode' in snake_data and snake_data['enforcement_mode'] is not None:
            snake_data['enforcement_mode'] = EnforcementMode.from_dict(snake_data['enforcement_mode'])
        if 'path_cache' in snake_data and snake_data['path_cache'] is not None:
            snake_data['path_cache'] = PathCacheConfig.from_dict(snake_data['path_cache'])
        if 'paths' in snake_data and snake_data['paths'] is not None:
            snake_data['paths'] = [
                PathConfig.from_dict(item) for item in snake_data['paths']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
