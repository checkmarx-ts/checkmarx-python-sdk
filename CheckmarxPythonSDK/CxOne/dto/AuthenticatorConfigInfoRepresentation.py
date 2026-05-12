from dataclasses import dataclass


@dataclass
class AuthenticatorConfigInfoRepresentation:
    help_text: ... = None
    name: ... = None
    properties: ... = None
    provider_id: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AuthenticatorConfigInfoRepresentation":
        return cls(
            help_text=item.get("helpText"),
            name=item.get("name"),
            properties=item.get("properties"),
            provider_id=item.get("providerId"),
        )
