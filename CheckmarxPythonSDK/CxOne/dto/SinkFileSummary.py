from dataclasses import dataclass


@dataclass
class SinkFileSummary:
    """

    Args:
        sink_file (str):
        count (int):
    """

    sink_file: str
    count: int
