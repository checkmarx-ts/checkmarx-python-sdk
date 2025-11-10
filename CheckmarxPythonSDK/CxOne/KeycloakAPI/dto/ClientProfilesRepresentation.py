from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ClientProfileRepresentation import ClientProfileRepresentation


@dataclass
class ClientProfilesRepresentation:
    profiles: Optional[List[ClientProfileRepresentation]] = None
    global_profiles: Optional[List[ClientProfileRepresentation]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.profiles is not None:
            value = [item.to_dict() for item in self.profiles]
            result['profiles'] = value
        if self.global_profiles is not None:
            value = [item.to_dict() for item in self.global_profiles]
            result['globalProfiles'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'profiles' in snake_data and snake_data['profiles'] is not None:
            snake_data['profiles'] = [
                ClientProfileRepresentation.from_dict(item) for item in snake_data['profiles']
            ]
        if 'global_profiles' in snake_data and snake_data['global_profiles'] is not None:
            snake_data['global_profiles'] = [
                ClientProfileRepresentation.from_dict(item) for item in snake_data['global_profiles']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
