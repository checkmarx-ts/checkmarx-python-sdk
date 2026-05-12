from dataclasses import dataclass


@dataclass
class SeverityCounter:
    severity: str = None
    counter: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "SeverityCounter":
        return cls(
            severity=item.get("severity"),
            counter=item.get("counter"),
        )
