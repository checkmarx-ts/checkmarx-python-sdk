from dataclasses import dataclass
from typing import List


@dataclass
class Preset:
    id: str = None
    name: str = None
    description: str = None
    custom: bool = None
    query_ids: List[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Preset":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            custom=item.get("custom"),
            query_ids=item.get("queryIds"),
        )
