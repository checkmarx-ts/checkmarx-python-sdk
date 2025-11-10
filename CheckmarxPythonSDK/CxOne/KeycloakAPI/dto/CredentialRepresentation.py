from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class CredentialRepresentation:
    id: Optional[str] = None
    type: Optional[str] = None
    user_label: Optional[str] = None
    created_date: Optional[int] = None
    secret_data: Optional[str] = None
    credential_data: Optional[str] = None
    priority: Optional[int] = None
    value: Optional[str] = None
    temporary: Optional[bool] = None
    device: Optional[str] = None
    hashed_salted_value: Optional[str] = None
    salt: Optional[str] = None
    hash_iterations: Optional[int] = None
    counter: Optional[int] = None
    algorithm: Optional[str] = None
    digits: Optional[int] = None
    period: Optional[int] = None
    config: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.type is not None:
            value = self.type
            result['type'] = value
        if self.user_label is not None:
            value = self.user_label
            result['userLabel'] = value
        if self.created_date is not None:
            value = self.created_date
            result['createdDate'] = value
        if self.secret_data is not None:
            value = self.secret_data
            result['secretData'] = value
        if self.credential_data is not None:
            value = self.credential_data
            result['credentialData'] = value
        if self.priority is not None:
            value = self.priority
            result['priority'] = value
        if self.value is not None:
            value = self.value
            result['value'] = value
        if self.temporary is not None:
            value = self.temporary
            result['temporary'] = value
        if self.device is not None:
            value = self.device
            result['device'] = value
        if self.hashed_salted_value is not None:
            value = self.hashed_salted_value
            result['hashedSaltedValue'] = value
        if self.salt is not None:
            value = self.salt
            result['salt'] = value
        if self.hash_iterations is not None:
            value = self.hash_iterations
            result['hashIterations'] = value
        if self.counter is not None:
            value = self.counter
            result['counter'] = value
        if self.algorithm is not None:
            value = self.algorithm
            result['algorithm'] = value
        if self.digits is not None:
            value = self.digits
            result['digits'] = value
        if self.period is not None:
            value = self.period
            result['period'] = value
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
