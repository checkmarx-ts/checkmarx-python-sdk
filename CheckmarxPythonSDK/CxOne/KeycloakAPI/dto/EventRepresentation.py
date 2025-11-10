from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class EventRepresentation:
    time: Optional[int] = None
    type: Optional[str] = None
    realm_id: Optional[str] = None
    client_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.time is not None:
            value = self.time
            result['time'] = value
        if self.type is not None:
            value = self.type
            result['type'] = value
        if self.realm_id is not None:
            value = self.realm_id
            result['realmId'] = value
        if self.client_id is not None:
            value = self.client_id
            result['clientId'] = value
        if self.user_id is not None:
            value = self.user_id
            result['userId'] = value
        if self.session_id is not None:
            value = self.session_id
            result['sessionId'] = value
        if self.ip_address is not None:
            value = self.ip_address
            result['ipAddress'] = value
        if self.error is not None:
            value = self.error
            result['error'] = value
        if self.details is not None:
            value = self.details
            result['details'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
