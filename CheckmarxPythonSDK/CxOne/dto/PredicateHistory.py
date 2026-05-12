from dataclasses import dataclass
from typing import List
from .PredicateWithCommentJSON import PredicateWithCommentJSON


@dataclass
class PredicateHistory:

    similarity_id: str = None
    project_id: str = None
    predicates: List[PredicateWithCommentJSON] = None
    total_count: int = None
