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


def construct_source_node_summary(item):
    return SourceNodeSummary(
        source_node=item.get("sourceNode"),
        count=item.get("count")
    )
