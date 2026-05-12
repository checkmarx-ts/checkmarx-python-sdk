from dataclasses import dataclass


@dataclass
class RequiredActionProviderRepresentation:
    alias: ... = None
    config: ... = None
    default_action: ... = None
    enabled: ... = None
    name: ... = None
    priority: ... = None
    provider_id: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "RequiredActionProviderRepresentation":
        return cls(
            alias=item.get("alias"),
            config=item.get("config"),
            default_action=item.get("defaultAction"),
            enabled=item.get("enabled"),
            name=item.get("name"),
            priority=item.get("priority"),
            provider_id=item.get("providerId"),
        )
