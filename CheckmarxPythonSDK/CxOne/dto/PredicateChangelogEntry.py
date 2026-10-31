from dataclasses import dataclass


@dataclass
class PredicateChangelogEntry:
    """One change entry in PredicateChangelogGroup.predicates (GET
    /api/sast-results-predicates/changelog).
    """
    change: str = None
    date: str = None
    user: str = None
    origin: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "PredicateChangelogEntry":
        if not item:
            return None
        return cls(
            change=item.get("change"),
            date=item.get("date"),
            user=item.get("user"),
            origin=item.get("origin"),
        )
