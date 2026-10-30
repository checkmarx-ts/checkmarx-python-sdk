from dataclasses import dataclass, field
from typing import List


@dataclass
class DastSimilarityIds:
    """A finding (by alert/similarity ID) to correlate or pentest.

    Used both as a request item (POST /correlations/scan, POST
    /pentest/scan) and as a response item (on CorrelationScanResponse/
    PentestScanResponse) — same shape either way.

    Attributes:
        alert_id (str): The finding's alert/similarity ID. Required.
        instance_ids (List[str]): Specific instance IDs of the finding,
            if narrowing to a subset.
    """
    alert_id: str = None
    instance_ids: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastSimilarityIds":
        return cls(
            alert_id=item.get("alertId"),
            instance_ids=list(item.get("instanceIds") or []),
        )

    def to_dict(self) -> dict:
        raw = {"alertId": self.alert_id, "instanceIds": self.instance_ids}
        return {k: v for k, v in raw.items() if v}
