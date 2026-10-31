from dataclasses import dataclass, field
from typing import List

from .CommentJSON import CommentJSON


@dataclass
class PredicateWithCommentsJSON:
    """An entry in LatestPredicateResponse.latest_predicate_per_project
    (GET /api/sast-results-predicates/{similarityId}/latest). Unlike
    PredicateWithCommentJSON (the history endpoint's per-predicate
    shape, singular commentJSON), this endpoint returns a plural
    commentsJSON array.
    """
    id: str = None
    similarity_id: str = None
    project_id: str = None
    severity: str = None
    state: str = None
    comment: str = None
    comments_json: List[CommentJSON] = field(default_factory=list)
    created_by: str = None
    created_at: str = None
    change_origin_type: int = None
    change_origin_name: str = None
    triggered_by: str = None  # only present when include-changed-by=true
    changed_by: str = None  # only present when include-changed-by=true

    @classmethod
    def from_dict(cls, item: dict) -> "PredicateWithCommentsJSON":
        if not item:
            return None
        return cls(
            id=item.get("ID"),
            similarity_id=item.get("similarityId"),
            project_id=item.get("projectId"),
            severity=item.get("severity"),
            state=item.get("state"),
            comment=item.get("comment"),
            comments_json=[
                CommentJSON.from_dict(c)
                for c in (item.get("commentsJSON") or [])
            ],
            created_by=item.get("createdBy"),
            created_at=item.get("createdAt"),
            change_origin_type=item.get("changeOriginType"),
            change_origin_name=item.get("changeOriginName"),
            triggered_by=item.get("triggeredBy"),
            changed_by=item.get("changedBy"),
        )
