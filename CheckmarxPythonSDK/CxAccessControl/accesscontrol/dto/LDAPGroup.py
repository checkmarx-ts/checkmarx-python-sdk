from dataclasses import dataclass
from typing import Optional


@dataclass
class LDAPGroup:
    name: Optional[str] = None
    dn: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "LDAPGroup":
        return cls(
            name=item.get("name"),
            dn=item.get("dn"),
        )
