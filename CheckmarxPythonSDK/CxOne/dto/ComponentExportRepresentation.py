from dataclasses import dataclass


@dataclass
class ComponentExportRepresentation:
    config: ... = None
    component_export_representation_id: ... = None
    name: ... = None
    provider_id: ... = None
    sub_components: ... = None
    sub_type: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ComponentExportRepresentation":
        return cls(
            config=item.get("config"),
            component_export_representation_id=item.get("id"),
            name=item.get("name"),
            provider_id=item.get("providerId"),
            sub_components=item.get("subComponents"),
            sub_type=item.get("subType"),
        )
