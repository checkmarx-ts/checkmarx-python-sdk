from dataclasses import dataclass


@dataclass
class ClientPolicyRepresentation:
    conditions: ... = None
    description: ... = None
    enabled: ... = None
    name: ... = None
    profiles: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientPolicyRepresentation":
        return cls(
            conditions=item.get("conditions"),
            description=item.get("description"),
            enabled=item.get("enabled"),
            name=item.get("name"),
            profiles=item.get("profiles"),
        )
