from dataclasses import dataclass
from typing import Optional


@dataclass
class CxScanFileCountOfLanguage:

    language: Optional[str] = None
    file_count: Optional[int] = None

    @classmethod
    def from_dict(cls, language: str, file_count: int) -> "CxScanFileCountOfLanguage":
        return cls(language=language, file_count=file_count)
