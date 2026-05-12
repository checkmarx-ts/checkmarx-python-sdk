from dataclasses import dataclass


@dataclass
class SeveritySummary:
    """

    Args:
        severity (str): Severity enum of a result. Enum: [ HIGH, MEDIUM, LOW, INFO ]
        count (int):
    """

    severity: str
    count: int
