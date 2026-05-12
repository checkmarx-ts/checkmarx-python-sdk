from dataclasses import dataclass


@dataclass
class SourceNodeSummary:
    """

    Args:
        source_node (str):
        count (int):
    """

    source_node: str
    count: int
