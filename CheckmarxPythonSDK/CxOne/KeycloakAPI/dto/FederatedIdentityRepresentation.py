from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class FederatedIdentityRepresentation:
    identity_provider: Optional[str] = None
    user_id: Optional[str] = None
    user_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.identity_provider is not None:
            value = self.identity_provider
            result['identityProvider'] = value
        if self.user_id is not None:
            value = self.user_id
            result['userId'] = value
        if self.user_name is not None:
            value = self.user_name
            result['userName'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
