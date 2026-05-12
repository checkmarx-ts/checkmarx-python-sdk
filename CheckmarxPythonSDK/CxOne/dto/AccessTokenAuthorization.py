from dataclasses import dataclass


@dataclass
class AccessTokenAuthorization:
    permissions: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AccessTokenAuthorization":
        return cls(
            permissions=item.get("permissions"),
        )
