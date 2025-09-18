from dataclasses import dataclass
from typing import List
from .PredicateWithCommentJSON import PredicateWithCommentJSON, construct_predicate_with_comment_json


@dataclass
class PredicateHistory:

    similarity_id: str = None
    project_id: str = None
    predicates: List[PredicateWithCommentJSON] = None
    total_count: int = None


def construct_predicate_history(item):
    return PredicateHistory(
        similarity_id=item.get("similarityId"),
        project_id=item.get("projectId"),
        predicates=[
           construct_predicate_with_comment_json(predicate) for predicate in item.get("predicates", [])
        ],
        total_count=item.get("totalCount")
    )
