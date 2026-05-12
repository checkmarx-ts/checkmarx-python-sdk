from dataclasses import dataclass


@dataclass
class ProjectCounter:
    """
    Attributes:
        value (str):
        count (int):
    """

    value: str = None
    count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "ProjectCounter":
        return cls(value=item.get("value"), count=item.get("count"))
