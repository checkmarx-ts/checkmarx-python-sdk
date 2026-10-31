from dataclasses import dataclass, field
from typing import List

from .PredicateInitialValues import PredicateInitialValues
from .PredicateWithCommentJSON import PredicateWithCommentJSON


@dataclass
class PredicateHistory:
    """Predicates for one similarity ID within one project. Also
    reused for GET /api/sast-results-predicates/ (predicates by
    attack vector id), whose predicateHistoryPerProject entries carry
    an extra attackVectorId field -- None for the plain
    /{similarityID} endpoint, which has no such field.
    """
    similarity_id: str = None
    project_id: str = None
    predicates: List[PredicateWithCommentJSON] = field(default_factory=list)
    total_count: int = None
    initial_predicate_values: PredicateInitialValues = None
    attack_vector_id: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "PredicateHistory":
        if not item:
            return None
        return cls(
            similarity_id=item.get("similarityId"),
            project_id=item.get("projectId"),
            predicates=[
                PredicateWithCommentJSON.from_dict(p)
                for p in (item.get("predicates") or [])
            ],
            total_count=item.get("totalCount"),
            initial_predicate_values=PredicateInitialValues.from_dict(
                item.get("initialPredicateValues")
            ),
            attack_vector_id=item.get("attackVectorId"),
        )
