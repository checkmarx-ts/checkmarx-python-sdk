from dataclasses import dataclass


@dataclass
class LanguageSummary:
    """

    Args:
        language (str):
        count (int):
    """
    language: str
    count: int


def construct_language_summary(item):
    return LanguageSummary(
        language=item.get("language"),
        count=item.get("count")
    )
