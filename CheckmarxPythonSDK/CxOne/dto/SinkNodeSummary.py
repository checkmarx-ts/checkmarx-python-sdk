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


def construct_sink_node_summary(item):
    return SinkNodeSummary(
        sink_node=item.get("sinkNode"),
        count=item.get("count")
    )
