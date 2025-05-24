from typing import List
from .PredicateWithCommentJSON import PredicateWithCommentJSON


class PredicateHistory(object):
    def __init__(self, similarity_id: str = None, project_id: str = None,
                 predicates: List[PredicateWithCommentJSON] = None, total_count: int = None):
        self.similarityId = similarity_id
        self.projectId = project_id
        self.predicates = predicates
        self.totalCount = total_count

    def __str__(self):
        return (f"PredicateHistory(similarityId={self.similarityId}, projectId={self.projectId}, "
                f"predicates={self.predicates}, totalCount={self.totalCount})")
