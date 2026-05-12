from dataclasses import dataclass
from typing import Optional


@dataclass
class CxProjectQueueSetting:

    queue_keep_mode: Optional[str] = None
    scans_type: Optional[str] = None
    include_scans_in_process: Optional[bool] = None
    identical_code_only: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxProjectQueueSetting":
        return cls(
            queue_keep_mode=item.get("queueKeepMode"),
            scans_type=item.get("scansType"),
            include_scans_in_process=item.get("includeScansInProcess"),
            identical_code_only=item.get("identicalCodeOnly"),
        )
