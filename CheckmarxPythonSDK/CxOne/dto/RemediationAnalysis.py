from dataclasses import dataclass


@dataclass
class RemediationAnalysis:
    """Explanation of the vulnerability and the recommended remediation."""

    what: str = None
    why: str = None
    how: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "RemediationAnalysis":
        return cls(
            what=item.get("what"),
            why=item.get("why"),
            how=item.get("how"),
        )
