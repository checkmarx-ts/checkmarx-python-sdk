from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class SocialLinkRepresentation:
    social_provider: Optional[str] = None
    social_user_id: Optional[str] = None
    social_username: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.social_provider is not None:
            value = self.social_provider
            result['socialProvider'] = value
        if self.social_user_id is not None:
            value = self.social_user_id
            result['socialUserId'] = value
        if self.social_username is not None:
            value = self.social_username
            result['socialUsername'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
