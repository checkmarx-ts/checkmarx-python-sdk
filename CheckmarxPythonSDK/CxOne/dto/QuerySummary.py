from dataclasses import dataclass


@dataclass
class QuerySummary:
    """

    Args:
        query_id (str):
        query_name (str):
        severity (str): Severity enum of a result. Enum: [ HIGH, MEDIUM, LOW, INFO ]
        count (int):
    """

    query_id: str = None
    query_name: str = None
    severity: str = None
    count: int = None
