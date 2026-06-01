from dataclasses import dataclass
from typing import Union
from .DastScanType import DastScanType


@dataclass
class DastScanFilter:
    """Shape for the `filter` and `match` query parameters of
    GET /api/dast/scans/scans. Same fields for both — `filter` is
    partial-match, `match` is exact-match.
    """
    initiator: str = None
    scan_type: Union[DastScanType, str] = None
    project_id: str = None

    def to_dict(self) -> dict:
        raw = {
            "initiator": self.initiator,
            "scantype": (
                self.scan_type.value if isinstance(self.scan_type, DastScanType)
                else self.scan_type
            ),
            "projectId": self.project_id,
        }
        return {k: v for k, v in raw.items() if v is not None}
