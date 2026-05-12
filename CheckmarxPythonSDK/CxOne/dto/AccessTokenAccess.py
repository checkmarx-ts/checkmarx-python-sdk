from dataclasses import dataclass


@dataclass
class AccessTokenAccess:
    roles: ... = None
    verify_caller: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AccessTokenAccess":
        return cls(
            roles=item.get("roles"),
            verify_caller=item.get("verify_caller"),
        )
