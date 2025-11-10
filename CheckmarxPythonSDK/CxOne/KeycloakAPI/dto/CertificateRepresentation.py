from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class CertificateRepresentation:
    private_key: Optional[str] = None
    public_key: Optional[str] = None
    certificate: Optional[str] = None
    kid: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.private_key is not None:
            value = self.private_key
            result['privateKey'] = value
        if self.public_key is not None:
            value = self.public_key
            result['publicKey'] = value
        if self.certificate is not None:
            value = self.certificate
            result['certificate'] = value
        if self.kid is not None:
            value = self.kid
            result['kid'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
