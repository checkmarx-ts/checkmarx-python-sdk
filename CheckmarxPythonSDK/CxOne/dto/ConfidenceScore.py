from dataclasses import dataclass


@dataclass
class ConfidenceScore:
    score: int = 0
    explanation: str = ""

    @classmethod
    def from_dict(cls, item: dict) -> "ConfidenceScore":
        return cls(
            score=item.get("score", 0),
            explanation=item.get("explanation", ""),
        )
