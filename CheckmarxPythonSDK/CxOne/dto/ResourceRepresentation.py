from dataclasses import dataclass


@dataclass
class ResourceRepresentation:
    resource_representation_id: ... = None
    attributes: ... = None
    display_name: ... = None
    icon_uri: ... = None
    name: ... = None
    owner_managed_access: ... = None
    scopes: ... = None
    resource_representation_type: ... = None
    uris: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ResourceRepresentation":
        return cls(
            resource_representation_id=item.get("id"),
            attributes=item.get("attributes"),
            display_name=item.get("displayName"),
            icon_uri=item.get("icon_uri"),
            name=item.get("name"),
            owner_managed_access=item.get("ownerManagedAccess"),
            scopes=item.get("scopes"),
            resource_representation_type=item.get("type"),
            uris=item.get("uris"),
        )
