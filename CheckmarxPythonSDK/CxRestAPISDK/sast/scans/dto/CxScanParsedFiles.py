from dataclasses import dataclass, field
from typing import List, Optional
from .CxScanParsedFilesMetric import CxScanParsedFilesMetric


@dataclass
class CxScanParsedFiles:

    id: Optional[int] = None
    scanned_files_per_language: Optional[List] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanParsedFiles":
        raw = item.get("scannedFilesPerLanguage") or {}
        metrics = (
            [
                CxScanParsedFilesMetric.from_dict(language=key, item=value)
                for key, value in raw.items()
            ]
            if isinstance(raw, dict)
            else list(raw)
        )
        return cls(
            id=item.get("id"),
            scanned_files_per_language=metrics,
        )
