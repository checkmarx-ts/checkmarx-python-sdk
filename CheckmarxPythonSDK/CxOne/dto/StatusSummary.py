from dataclasses import dataclass


@dataclass
class StatusSummary:
    """

    Args:
        status (str): Status enum of a result Enum: [ NEW, RECURRENT ]
        count (int):
    """

    status: str
    count: int
