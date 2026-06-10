from dataclasses import dataclass


@dataclass
class PredicateInitialValues:
    """Initial state/severity before triage."""
    state: str = None
    severity: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "PredicateInitialValues":
        if not item:
            return None
        return cls(state=item.get("state"), severity=item.get("severity"))
