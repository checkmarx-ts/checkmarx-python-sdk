from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class UserSessionRepresentation:
    id: Optional[str] = None
    username: Optional[str] = None
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    start: Optional[int] = None
    last_access: Optional[int] = None
    remember_me: Optional[bool] = None
    clients: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.username is not None:
            value = self.username
            result['username'] = value
        if self.user_id is not None:
            value = self.user_id
            result['userId'] = value
        if self.ip_address is not None:
            value = self.ip_address
            result['ipAddress'] = value
        if self.start is not None:
            value = self.start
            result['start'] = value
        if self.last_access is not None:
            value = self.last_access
            result['lastAccess'] = value
        if self.remember_me is not None:
            value = self.remember_me
            result['rememberMe'] = value
        if self.clients is not None:
            value = self.clients
            result['clients'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
