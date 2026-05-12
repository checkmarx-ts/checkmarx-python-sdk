from dataclasses import dataclass


@dataclass
class ConfigPropertyRepresentation:
    default_value: ... = None
    help_text: ... = None
    label: ... = None
    name: ... = None
    options: ... = None
    secret: ... = None
    config_property_representation_type: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ConfigPropertyRepresentation":
        return cls(
            default_value=item.get("defaultValue"),
            help_text=item.get("helpText"),
            label=item.get("label"),
            name=item.get("name"),
            options=item.get("options"),
            secret=item.get("secret"),
            config_property_representation_type=item.get("type"),
        )
