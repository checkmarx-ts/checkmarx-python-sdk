from dataclasses import dataclass
from typing import List


@dataclass
class SubCheck:
    """
    Args:
        name (str):
        success (bool):
        errors (list of str):
    """

    name: str
    success: bool
    errors: List[str]

    @classmethod
    def from_dict(cls, item: dict) -> "SubCheck":
        return cls(
            name=item.get("name"),
            success=item.get("success"),
            errors=item.get("errors"),
        )
