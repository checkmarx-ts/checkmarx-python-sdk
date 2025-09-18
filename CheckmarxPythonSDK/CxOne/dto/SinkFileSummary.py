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


def construct_sink_file_summary(item):
    return SinkFileSummary(
        sink_file=item.get("sinkFile"),
        count=item.get("count")
    )
