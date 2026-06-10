from dataclasses import dataclass


@dataclass
class CommentJSON:
    id: str = None
    date: str = None
    user: str = None
    content: str = None
    is_deleted: bool = None

    @classmethod
    def from_dict(cls, item: dict) -> "CommentJSON":
        if not item:
            return None
        return cls(
            id=item.get("id"),
            date=item.get("date"),
            user=item.get("user"),
            content=item.get("content"),
            is_deleted=item.get("isDeleted", False),
        )
