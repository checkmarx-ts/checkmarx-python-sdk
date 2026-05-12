# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxSupportedLanguage:
    """
    The support status of a given programming language
    """

    is_supported: Optional[bool] = None
    language: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxSupportedLanguage":
        return cls(
            is_supported=item.get("isSupported"),
            language=item.get("language"),
        )
