from dataclasses import dataclass


@dataclass
class CommentJSON:
    id: str = None
    date: str = None
    user: str = None
    content: str = None
    is_deleted: bool = None


def construct_comment_json(item):
    return CommentJSON(
        id=item.get("id"),
        date=item.get("date"),
        user=item.get("user"),
        content=item.get("content"),
        is_deleted=item.get("isDeleted")
    )
