from dataclasses import dataclass


@dataclass
class ScopeRepresentation:
    display_name: ... = None
    icon_uri: ... = None
    scope_representation_id: ... = None
    name: ... = None
    policies: ... = None
    resources: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScopeRepresentation":
        return cls(
            display_name=item.get("displayName"),
            icon_uri=item.get("iconUri"),
            scope_representation_id=item.get("id"),
            name=item.get("name"),
            policies=item.get("policies"),
            resources=item.get("resources"),
        )
