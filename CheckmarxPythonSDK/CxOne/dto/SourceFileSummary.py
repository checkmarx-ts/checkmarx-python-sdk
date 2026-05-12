from dataclasses import dataclass


@dataclass
class SourceFileSummary:
    """

    Args:
        source_file (str):
        count (int):
    """

    source_file: str
    count: int
