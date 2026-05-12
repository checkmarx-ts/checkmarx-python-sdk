from dataclasses import dataclass


@dataclass
class SinkNodeSummary:
    """

    Args:
        sink_node (str):
        count (int):
    """

    sink_node: str
    count: int
