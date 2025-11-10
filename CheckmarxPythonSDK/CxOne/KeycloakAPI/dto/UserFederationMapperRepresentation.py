from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class UserFederationMapperRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    federation_provider_display_name: Optional[str] = None
    federation_mapper_type: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.federation_provider_display_name is not None:
            value = self.federation_provider_display_name
            result['federationProviderDisplayName'] = value
        if self.federation_mapper_type is not None:
            value = self.federation_mapper_type
            result['federationMapperType'] = value
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
