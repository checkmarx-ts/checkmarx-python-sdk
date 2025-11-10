from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class UserFederationProviderRepresentation:
    id: Optional[str] = None
    display_name: Optional[str] = None
    provider_name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    priority: Optional[int] = None
    full_sync_period: Optional[int] = None
    changed_sync_period: Optional[int] = None
    last_sync: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.display_name is not None:
            value = self.display_name
            result['displayName'] = value
        if self.provider_name is not None:
            value = self.provider_name
            result['providerName'] = value
        if self.config is not None:
            value = self.config
            result['config'] = value
        if self.priority is not None:
            value = self.priority
            result['priority'] = value
        if self.full_sync_period is not None:
            value = self.full_sync_period
            result['fullSyncPeriod'] = value
        if self.changed_sync_period is not None:
            value = self.changed_sync_period
            result['changedSyncPeriod'] = value
        if self.last_sync is not None:
            value = self.last_sync
            result['lastSync'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
