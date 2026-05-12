from dataclasses import dataclass


@dataclass
class Group:
    id: str = None
    name: str = None
    brief_name: str = None
    parent_id: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "Group":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            brief_name=item.get("briefName"),
            parent_id=item.get("parentId"),
        )
