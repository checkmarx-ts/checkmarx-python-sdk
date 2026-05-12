# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxSourceSettingsLink:
    """
    source settings link
    """

    source_settings_link_type: Optional[str] = None
    rel: Optional[str] = None
    uri: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxSourceSettingsLink":
        return cls(
            source_settings_link_type=item.get("type"),
            rel=item.get("rel"),
            uri=item.get("uri"),
        )
