from dataclasses import dataclass, field
from typing import List
from .MethodParameter import MethodParameter


@dataclass
class MethodInfo:
    lang: str = None
    name: str = None
    member_of: str = None
    documentation: str = None
    return_type: str = None
    kind: str = None
    parameters: List[MethodParameter] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "MethodInfo":
        return cls(
            lang=item.get("lang"),
            name=item.get("name"),
            member_of=item.get("memberOf "),
            documentation=item.get("documentation"),
            return_type=item.get("returnType"),
            kind=item.get("kind"),
            parameters=[
                MethodParameter.from_dict(p) for p in (item.get("parameters") or [])
            ],
        )
