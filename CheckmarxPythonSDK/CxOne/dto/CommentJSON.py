from dataclasses import dataclass


@dataclass
class CommentJSON:
    id: str = None
    date: str = None
    user: str = None
    content: str = None
    is_deleted: bool = None
