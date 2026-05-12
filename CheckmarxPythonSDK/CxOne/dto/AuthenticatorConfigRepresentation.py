from dataclasses import dataclass


@dataclass
class AuthenticatorConfigRepresentation:
    alias: ... = None
    config: ... = None
    authenticator_config_representation_id: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AuthenticatorConfigRepresentation":
        return cls(
            alias=item.get("alias"),
            config=item.get("config"),
            authenticator_config_representation_id=item.get("id"),
        )
