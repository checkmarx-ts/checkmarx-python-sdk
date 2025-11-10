from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ResourceRepresentationOwner import ResourceRepresentationOwner
from .ScopeRepresentation import ScopeRepresentation


@dataclass
class ResourceRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    uris: Optional[List[str]] = None
    type: Optional[str] = None
    scopes: Optional[List[ScopeRepresentation]] = None
    icon_uri: Optional[str] = None
    owner: Optional[ResourceRepresentationOwner] = None
    owner_managed_access: Optional[bool] = None
    display_name: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    uri: Optional[str] = None
    scopes_uma: Optional[List[ScopeRepresentation]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.uris is not None:
            value = self.uris
            result['uris'] = value
        if self.type is not None:
            value = self.type
            result['type'] = value
        if self.scopes is not None:
            value = [item.to_dict() for item in self.scopes]
            result['scopes'] = value
        if self.icon_uri is not None:
            value = self.icon_uri
            result['iconUri'] = value
        if self.owner is not None:
            value = self.owner.to_dict()
            result['owner'] = value
        if self.owner_managed_access is not None:
            value = self.owner_managed_access
            result['ownerManagedAccess'] = value
        if self.display_name is not None:
            value = self.display_name
            result['displayName'] = value
        if self.attributes is not None:
            value = self.attributes
            result['attributes'] = value
        if self.uri is not None:
            value = self.uri
            result['uri'] = value
        if self.scopes_uma is not None:
            value = [item.to_dict() for item in self.scopes_uma]
            result['scopesUma'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'owner' in snake_data and snake_data['owner'] is not None:
            snake_data['owner'] = ResourceRepresentationOwner.from_dict(snake_data['owner'])
        if 'scopes' in snake_data and snake_data['scopes'] is not None:
            snake_data['scopes'] = [
                ScopeRepresentation.from_dict(item) for item in snake_data['scopes']
            ]
        if 'scopes_uma' in snake_data and snake_data['scopes_uma'] is not None:
            snake_data['scopes_uma'] = [
                ScopeRepresentation.from_dict(item) for item in snake_data['scopes_uma']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
