from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .KeyMetadataRepresentation import KeyMetadataRepresentation


@dataclass
class KeysMetadataRepresentation:
    active: Optional[Dict[str, Any]] = None
    keys: Optional[List[KeyMetadataRepresentation]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.active is not None:
            value = self.active
            result['active'] = value
        if self.keys is not None:
            value = [item.to_dict() for item in self.keys]
            result['keys'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'keys' in snake_data and snake_data['keys'] is not None:
            snake_data['keys'] = [
                KeyMetadataRepresentation.from_dict(item) for item in snake_data['keys']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
