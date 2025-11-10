from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class KeyStoreConfig:
    realm_certificate: Optional[bool] = None
    store_password: Optional[str] = None
    key_password: Optional[str] = None
    key_alias: Optional[str] = None
    realm_alias: Optional[str] = None
    format: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.realm_certificate is not None:
            value = self.realm_certificate
            result['realmCertificate'] = value
        if self.store_password is not None:
            value = self.store_password
            result['storePassword'] = value
        if self.key_password is not None:
            value = self.key_password
            result['keyPassword'] = value
        if self.key_alias is not None:
            value = self.key_alias
            result['keyAlias'] = value
        if self.realm_alias is not None:
            value = self.realm_alias
            result['realmAlias'] = value
        if self.format is not None:
            value = self.format
            result['format'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
