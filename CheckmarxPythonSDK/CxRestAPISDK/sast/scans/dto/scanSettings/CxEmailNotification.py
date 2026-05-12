# encoding: utf-8
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CxEmailNotification:
    """
    email notification
    """

    failed_scan: Optional[List[str]] = None
    before_scan: Optional[List[str]] = None
    after_scan: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxEmailNotification":
        return cls(
            failed_scan=item.get("failedScan"),
            before_scan=item.get("beforeScan"),
            after_scan=item.get("afterScan"),
        )
