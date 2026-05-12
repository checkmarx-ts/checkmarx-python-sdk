# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxScanReportStatus:
    """
    scan report status
    """

    class Status:
        def __init__(self, status_id, value):
            """

            Args:
                status_id (int):
                value (str):
            """
            self.id = status_id
            self.value = value

    link: Optional[object] = None
    content_type: Optional[str] = None
    status: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanReportStatus":
        status_dict = item.get("status") or {}
        return cls(
            link=item.get("link"),
            content_type=item.get("contentType"),
            status=CxScanReportStatus.Status(
                status_id=status_dict.get("id"),
                value=status_dict.get("value"),
            ),
        )
