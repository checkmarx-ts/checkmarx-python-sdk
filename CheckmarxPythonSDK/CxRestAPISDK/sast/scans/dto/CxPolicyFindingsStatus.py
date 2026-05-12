# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxPolicyFindingsStatus:
    """
    policy finding status
    """

    project: Optional[object] = None
    scan: Optional[object] = None
    status: Optional[str] = None
    last_sync: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxPolicyFindingsStatus":
        return cls(
            project=item.get("project"),
            scan=item.get("scan"),
            status=item.get("status"),
            last_sync=item.get("lastSync"),
        )
