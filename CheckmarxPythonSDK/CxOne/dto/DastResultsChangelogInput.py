from dataclasses import dataclass
from typing import List, Union
from .DastResultSeverity import DastResultSeverity
from .DastResultState import DastResultState
from .DastResultsChangelogType import DastResultsChangelogType


@dataclass
class DastResultsChangelogInput:
    """Request body for POST /api/dast/mfe-results/changelog.

    Required: similarity_id_2 (1–1000 entries), environment_id, scan_id.
    All others are optional.

    The wire field name for the result-ids array is `similarityID2`
    (camelCase, capital ID, trailing 2) — inconsistent with the rest
    of the results API which uses snake_case, but that's how the doc
    spells it.

    Note on the `type` field:
      - type=INSTANCE → similarityID2 array targets specific instances
      - type=ALERT    → alert_similarity_id is required; updates all
                        instances of an alert
    """
    similarity_id_2: List[str] = None
    environment_id: str = None
    scan_id: str = None
    severity: Union[DastResultSeverity, str] = None
    state: Union[DastResultState, str] = None
    note: str = None
    type: Union[DastResultsChangelogType, str] = None
    alert_similarity_id: str = None
    custom_state_id: int = None

    @staticmethod
    def _val(v):
        return v.value if hasattr(v, "value") else v

    def to_dict(self) -> dict:
        raw = {
            "similarityID2": self.similarity_id_2,
            "environment_id": self.environment_id,
            "scan_id": self.scan_id,
            "severity": self._val(self.severity),
            "state": self._val(self.state),
            "note": self.note,
            "type": self._val(self.type),
            "alert_similarity_id": self.alert_similarity_id,
            "custom_state_id": self.custom_state_id,
        }
        return {k: v for k, v in raw.items() if v is not None}
