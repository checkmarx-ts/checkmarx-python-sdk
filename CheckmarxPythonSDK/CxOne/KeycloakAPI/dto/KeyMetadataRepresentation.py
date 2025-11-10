from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .KeyUse import KeyUse


@dataclass
class KeyMetadataRepresentation:
    provider_id: Optional[str] = None
    provider_priority: Optional[int] = None
    kid: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    algorithm: Optional[str] = None
    public_key: Optional[str] = None
    certificate: Optional[str] = None
    use: Optional[KeyUse] = None
    valid_to: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.provider_id is not None:
            value = self.provider_id
            result['providerId'] = value
        if self.provider_priority is not None:
            value = self.provider_priority
            result['providerPriority'] = value
        if self.kid is not None:
            value = self.kid
            result['kid'] = value
        if self.status is not None:
            value = self.status
            result['status'] = value
        if self.type is not None:
            value = self.type
            result['type'] = value
        if self.algorithm is not None:
            value = self.algorithm
            result['algorithm'] = value
        if self.public_key is not None:
            value = self.public_key
            result['publicKey'] = value
        if self.certificate is not None:
            value = self.certificate
            result['certificate'] = value
        if self.use is not None:
            value = self.use.to_dict()
            result['use'] = value
        if self.valid_to is not None:
            value = self.valid_to
            result['validTo'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'use' in snake_data and snake_data['use'] is not None:
            snake_data['use'] = KeyUse.from_dict(snake_data['use'])
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
