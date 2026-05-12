# encoding: utf-8
from dataclasses import dataclass, field
from typing import List, Optional
from .CxLanguageState import CxLanguageState


@dataclass
class CxScanState:
    """
    scan state, used in CxScanDetail
    """

    path: Optional[str] = None
    source_id: Optional[str] = None
    files_count: Optional[int] = None
    lines_of_code: Optional[int] = None
    failed_lines_of_code: Optional[int] = None
    cx_version: Optional[str] = None
    language_state_collection: List[CxLanguageState] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanState":
        return cls(
            path=item.get("path"),
            source_id=item.get("sourceId"),
            files_count=item.get("filesCount"),
            lines_of_code=item.get("linesOfCode"),
            failed_lines_of_code=item.get("failedLinesOfCode"),
            cx_version=item.get("cxVersion"),
            language_state_collection=[
                CxLanguageState.from_dict(ls)
                for ls in (item.get("languageStateCollection") or [])
            ],
        )
