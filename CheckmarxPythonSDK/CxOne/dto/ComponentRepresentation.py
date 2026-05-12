from dataclasses import dataclass


@dataclass
class ComponentRepresentation:
    config: ... = None
    component_representation_id: ... = None
    name: ... = None
    parent_id: ... = None
    provider_id: ... = None
    provider_type: ... = None
    sub_type: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ComponentRepresentation":
        return cls(
            config=item.get("config"),
            component_representation_id=item.get("id"),
            name=item.get("name"),
            parent_id=item.get("parentId"),
            provider_id=item.get("providerId"),
            provider_type=item.get("providerType"),
            sub_type=item.get("subType"),
        )
