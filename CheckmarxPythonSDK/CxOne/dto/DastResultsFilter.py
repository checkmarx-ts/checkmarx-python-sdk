from dataclasses import dataclass
from typing import Union
from .DastResultStatus import DastResultStatus
from .DastResultState import DastResultState


@dataclass
class DastResultsFilter:
    """Shape for the `filter` query parameter of
    GET /api/dast/mfe-results/results/{scan_id}.

    Partial-match across severity / path / name / method / status /
    state / url / owasp / alert_similarity_id. The wire keys are
    snake_case (the doc shows them that way too, and this endpoint
    consistently uses snake_case in responses).
    """
    severity: str = None
    path: str = None
    name: str = None
    method: str = None
    status: Union[DastResultStatus, str] = None
    state: Union[DastResultState, str] = None
    url: str = None
    owasp: str = None
    alert_similarity_id: str = None

    def to_dict(self) -> dict:
        raw = {
            "severity": self.severity,
            "path": self.path,
            "name": self.name,
            "method": self.method,
            "status": (
                self.status.value if isinstance(self.status, DastResultStatus)
                else self.status
            ),
            "state": (
                self.state.value if isinstance(self.state, DastResultState)
                else self.state
            ),
            "url": self.url,
            "owasp": self.owasp,
            "alert_similarity_id": self.alert_similarity_id,
        }
        return {k: v for k, v in raw.items() if v is not None}
