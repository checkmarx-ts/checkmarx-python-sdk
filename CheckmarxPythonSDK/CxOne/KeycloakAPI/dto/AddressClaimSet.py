from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class AddressClaimSet:
    formatted: Optional[str] = None
    street_address: Optional[str] = None
    locality: Optional[str] = None
    region: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.formatted is not None:
            value = self.formatted
            result['formatted'] = value
        if self.street_address is not None:
            value = self.street_address
            result['streetAddress'] = value
        if self.locality is not None:
            value = self.locality
            result['locality'] = value
        if self.region is not None:
            value = self.region
            result['region'] = value
        if self.postal_code is not None:
            value = self.postal_code
            result['postalCode'] = value
        if self.country is not None:
            value = self.country
            result['country'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
