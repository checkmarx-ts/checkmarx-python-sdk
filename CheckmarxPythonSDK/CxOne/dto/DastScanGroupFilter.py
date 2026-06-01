from dataclasses import dataclass
from typing import Union
from .DastScanType import DastScanType


@dataclass
class DastScanGroupFilter:
    """Shape for the `filter` query parameter of
    GET /api/dast/scans/scans/groups.

    Different from DastScanFilter (which has project_id and no
    risk_rating). The doc shows three casings for the wire keys
    (Initiator / scanType / RiskRating); we send the lowercase
    forms that have been verified working on the env-filter endpoint.
    """
    initiator: str = None
    scan_type: Union[DastScanType, str] = None
    risk_rating: str = None

    def to_dict(self) -> dict:
        raw = {
            "initiator": self.initiator,
            "scantype": (
                self.scan_type.value if isinstance(self.scan_type, DastScanType)
                else self.scan_type
            ),
            "riskrating": self.risk_rating,
        }
        return {k: v for k, v in raw.items() if v is not None}
