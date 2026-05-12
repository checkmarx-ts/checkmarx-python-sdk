from dataclasses import dataclass


@dataclass
class AccessTokenCertConf:
    x5t: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AccessTokenCertConf":
        return cls(
            x5t=item.get("x5t"),
        )
