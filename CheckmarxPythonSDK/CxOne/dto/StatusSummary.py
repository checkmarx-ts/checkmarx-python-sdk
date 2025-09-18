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


def construct_status_summary(item):
    return StatusSummary(
        status=item.get("status"),
        count=item.get("count")
    )
