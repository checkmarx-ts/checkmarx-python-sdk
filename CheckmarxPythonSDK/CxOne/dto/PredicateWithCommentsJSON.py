from dataclasses import dataclass
from typing import List
from .CommentJSON import CommentJSON


@dataclass
class PredicateWithCommentsJSON:
    id: str = None
    similarity_id: str = None
    project_id: str = None
    severity: str = (None,)
    state: str = None
    comment: str = None
    comments_json: List[CommentJSON] = None
    created_by: str = None
    created_at: str = None
    change_origin_type: int = None
    change_origin_name: str = None
