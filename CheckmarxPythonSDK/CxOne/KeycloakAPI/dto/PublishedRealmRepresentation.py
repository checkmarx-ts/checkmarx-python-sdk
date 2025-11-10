from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class PublishedRealmRepresentation:
    realm: Optional[str] = None
    public_key: Optional[str] = None
    token_service: Optional[str] = None
    account_service: Optional[str] = None
    tokens_not_before: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.realm is not None:
            value = self.realm
            result['realm'] = value
        if self.public_key is not None:
            value = self.public_key
            result['publicKey'] = value
        if self.token_service is not None:
            value = self.token_service
            result['tokenService'] = value
        if self.account_service is not None:
            value = self.account_service
            result['accountService'] = value
        if self.tokens_not_before is not None:
            value = self.tokens_not_before
            result['tokensNotBefore'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
