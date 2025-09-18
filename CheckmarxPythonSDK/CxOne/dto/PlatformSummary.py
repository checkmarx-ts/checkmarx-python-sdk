from dataclasses import dataclass


@dataclass
class PlatformSummary:
    """

    Attributes:
        platform (str):
        count (int):
    """
    platform: str
    count: int


def construct_platform_summary(item):
    return PlatformSummary(
        platform=item.get("platform"),
        count=item.get("count")
    )
