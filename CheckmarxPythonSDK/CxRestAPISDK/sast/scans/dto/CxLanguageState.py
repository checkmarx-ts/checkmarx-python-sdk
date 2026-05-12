# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxLanguageState:
    """
    language state
    """

    language_id: Optional[int] = None
    language_name: Optional[str] = None
    language_hash: Optional[str] = None
    state_creation_date: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxLanguageState":
        return cls(
            language_id=item.get("languageID"),  # Note: uppercase ID in API
            language_name=item.get("languageName"),
            language_hash=item.get("languageHash"),
            state_creation_date=item.get("stateCreationDate"),
        )
