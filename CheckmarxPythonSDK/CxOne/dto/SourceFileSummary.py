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


def construct_source_file_summary(item):
    return SourceFileSummary(
        source_file=item.get("sourceFile"),
        count=item.get("count")
    )
