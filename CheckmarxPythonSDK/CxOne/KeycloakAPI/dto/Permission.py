from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class Permission:
    rsid: Optional[str] = None
    rsname: Optional[str] = None
    scopes: Optional[List[str]] = None
    claims: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.rsid is not None:
            value = self.rsid
            result['rsid'] = value
        if self.rsname is not None:
            value = self.rsname
            result['rsname'] = value
        if self.scopes is not None:
            value = self.scopes
            result['scopes'] = value
        if self.claims is not None:
            value = self.claims
            result['claims'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
