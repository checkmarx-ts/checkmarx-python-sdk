# encoding: utf-8
from dataclasses import dataclass, field
from typing import List, Optional
from .CxEngineDedication import CxEngineDedication
from .CxEngineServerStatus import CxEngineServerStatus


@dataclass
class CxEngineServer:
    """
    engine server
    """

    id: Optional[int] = None
    name: Optional[str] = None
    uri: Optional[str] = None
    min_loc: Optional[int] = None
    max_loc: Optional[int] = None
    max_scans: Optional[int] = None
    cx_version: Optional[str] = None
    operating_system: Optional[str] = None
    status: Optional[CxEngineServerStatus] = None
    link: Optional[object] = None
    offline_reason_code: Optional[str] = None
    offline_reason_message: Optional[str] = None
    offline_reason_message_parameters: Optional[str] = None
    dedications: List[CxEngineDedication] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "CxEngineServer":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            uri=item.get("uri"),
            min_loc=item.get("minLoc"),
            max_loc=item.get("maxLoc"),
            max_scans=item.get("maxScans"),
            cx_version=item.get("cxVersion"),
            operating_system=item.get("operatingSystem"),
            status=CxEngineServerStatus.from_dict(item.get("status") or {}),
            link=item.get("link"),
            offline_reason_code=item.get("offlineReasonCode"),
            offline_reason_message=item.get("offlineReasonMessage"),
            offline_reason_message_parameters=item.get(
                "offlineReasonMessageParameters"
            ),
            dedications=[
                CxEngineDedication.from_dict(d) for d in (item.get("dedications") or [])
            ],
        )
