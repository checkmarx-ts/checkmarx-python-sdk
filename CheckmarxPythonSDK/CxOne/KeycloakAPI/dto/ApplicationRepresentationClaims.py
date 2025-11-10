from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class ApplicationRepresentationClaims:
    name: Optional[bool] = None
    username: Optional[bool] = None
    profile: Optional[bool] = None
    picture: Optional[bool] = None
    website: Optional[bool] = None
    email: Optional[bool] = None
    gender: Optional[bool] = None
    locale: Optional[bool] = None
    address: Optional[bool] = None
    phone: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.username is not None:
            value = self.username
            result['username'] = value
        if self.profile is not None:
            value = self.profile
            result['profile'] = value
        if self.picture is not None:
            value = self.picture
            result['picture'] = value
        if self.website is not None:
            value = self.website
            result['website'] = value
        if self.email is not None:
            value = self.email
            result['email'] = value
        if self.gender is not None:
            value = self.gender
            result['gender'] = value
        if self.locale is not None:
            value = self.locale
            result['locale'] = value
        if self.address is not None:
            value = self.address
            result['address'] = value
        if self.phone is not None:
            value = self.phone
            result['phone'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
