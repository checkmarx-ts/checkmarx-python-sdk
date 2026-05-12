from dataclasses import dataclass


@dataclass
class AstIdWithName:
    """
    Attributes:
        id (str):
        name (str):
        brief_name (str):
        parent_id (str)
    """

    id: str
    name: str
    brief_name: str
    parent_id: str

    @classmethod
    def from_dict(cls, item: dict) -> "AstIdWithName":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            brief_name=item.get("briefName"),
            parent_id=item.get("parentId"),
        )
