from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class GroupRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[str] = None
    sub_group_count: Optional[int] = None
    sub_groups: Optional[List[Self]] = None
    attributes: Optional[Dict[str, Any]] = None
    realm_roles: Optional[List[str]] = None
    client_roles: Optional[Dict[str, Any]] = None
    access: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.path is not None:
            value = self.path
            result['path'] = value
        if self.parent_id is not None:
            value = self.parent_id
            result['parentId'] = value
        if self.sub_group_count is not None:
            value = self.sub_group_count
            result['subGroupCount'] = value
        if self.sub_groups is not None:
            value = self.sub_groups
            result['subGroups'] = value
        if self.attributes is not None:
            value = self.attributes
            result['attributes'] = value
        if self.realm_roles is not None:
            value = self.realm_roles
            result['realmRoles'] = value
        if self.client_roles is not None:
            value = self.client_roles
            result['clientRoles'] = value
        if self.access is not None:
            value = self.access
            result['access'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
