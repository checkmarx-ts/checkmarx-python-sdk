from dataclasses import dataclass, field
from typing import List

from .PredicateChangelogEntry import PredicateChangelogEntry


@dataclass
class PredicateChangelogGroup:
    """An entry in PredicatesChangelogResponse.results -- all change
    entries for one similarity id. The public doc's schema shows
    `results` as a flat array of change entries; the live response
    actually groups them by similarityId, as modeled here.
    """
    similarity_id: str = None
    predicates: List[PredicateChangelogEntry] = field(default_factory=list)
    total_count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "PredicateChangelogGroup":
        if not item:
            return None
        return cls(
            similarity_id=item.get("similarityId"),
            predicates=[
                PredicateChangelogEntry.from_dict(p)
                for p in (item.get("predicates") or [])
            ],
            total_count=item.get("totalCount"),
        )
