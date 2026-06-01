from dataclasses import dataclass
from typing import List, Union
from .DastScanType import DastScanType


@dataclass
class DastScanUpdate:
    """Request body for PUT /api/dast/scans/scan.

    Edits the configuration of an existing scan. `scan_id` and
    `environment_id` are required by the API; the wire keys are
    `scanId` and `environmentID` (note the inconsistent casing —
    that's how the API documents it).
    """
    scan_id: str = None
    environment_id: str = None
    scan_type: Union[DastScanType, str] = None
    groups: List[str] = None
    tags: List[str] = None

    def to_dict(self) -> dict:
        raw = {
            "scanId": self.scan_id,
            "environmentID": self.environment_id,
            "scanType": (
                self.scan_type.value if isinstance(self.scan_type, DastScanType)
                else self.scan_type
            ),
            "groups": self.groups,
            "tags": self.tags,
        }
        return {k: v for k, v in raw.items() if v is not None}
