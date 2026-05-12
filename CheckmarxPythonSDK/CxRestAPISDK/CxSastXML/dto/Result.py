from dataclasses import dataclass
from typing import Optional

from .Path import Path


@dataclass
class Result:
    node_id: Optional[int] = None
    file_name: Optional[str] = None
    status: Optional[str] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    false_positive: Optional[str] = None
    severity: Optional[str] = None
    assign_to_user: Optional[str] = None
    state: Optional[str] = None
    remark: Optional[str] = None
    deep_link: Optional[str] = None
    severity_index: Optional[int] = None
    status_index: Optional[int] = None
    detection_date: Optional[str] = None
    path: Optional[Path] = None

    @classmethod
    def from_dict(cls, item: dict, path=None) -> "Result":
        return cls(
            node_id=int(item.get("NodeId")),
            file_name=item.get("FileName"),
            status=item.get("Status"),
            line_number=int(item.get("Line")),
            column_number=int(item.get("Column")),
            false_positive=item.get("FalsePositive"),
            severity=item.get("Severity"),
            assign_to_user=item.get("AssignToUser"),
            state=item.get("State"),
            remark=item.get("Remark"),
            deep_link=item.get("DeepLink"),
            severity_index=int(item.get("SeverityIndex")),
            status_index=int(item.get("StatusIndex")),
            detection_date=item.get("DetectionDate"),
            path=path,
        )
