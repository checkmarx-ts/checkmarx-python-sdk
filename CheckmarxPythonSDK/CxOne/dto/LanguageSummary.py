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
