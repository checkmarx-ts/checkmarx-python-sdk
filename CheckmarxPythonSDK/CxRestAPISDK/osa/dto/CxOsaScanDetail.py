# encoding: utf-8
from dataclasses import dataclass, field
from typing import List, Optional
from .CxOsaState import CxOsaState


@dataclass
class CxOsaScanDetail:
    """
    osa scan detail
    """

    findings_status: Optional[str] = None
    id: Optional[str] = None
    start_analyze_time: Optional[str] = None
    end_analyze_time: Optional[str] = None
    origin: Optional[str] = None
    source_code_origin: Optional[str] = None
    state: Optional[CxOsaState] = None
    shared_source_location_paths: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "CxOsaScanDetail":
        return cls(
            findings_status=item.get("findingsStatus"),
            id=item.get("id"),
            start_analyze_time=item.get("startAnalyzeTime"),
            end_analyze_time=item.get("endAnalyzeTime"),
            origin=item.get("origin"),
            source_code_origin=item.get("sourceCodeOrigin"),
            state=CxOsaState.from_dict(item.get("state") or {}),
            shared_source_location_paths=list(
                item.get("sharedSourceLocationPaths") or []
            ),
        )
