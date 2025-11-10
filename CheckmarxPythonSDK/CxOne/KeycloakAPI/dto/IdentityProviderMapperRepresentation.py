from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class IdentityProviderMapperRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    identity_provider_alias: Optional[str] = None
    identity_provider_mapper: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.identity_provider_alias is not None:
            value = self.identity_provider_alias
            result['identityProviderAlias'] = value
        if self.identity_provider_mapper is not None:
            value = self.identity_provider_mapper
            result['identityProviderMapper'] = value
        if self.config is not None:
            value = self.config
            result['config'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
