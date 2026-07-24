from dataclasses import dataclass, field
from typing import List

from .RemediationResult import RemediationResult


@dataclass
class AiRemediationDetails:
    """Response from GET /api/remediation/remediation-details/{scan_id}/{result_id}.

    Contains the remediation details for one or more vulnerability results in
    a scan. If remediation is still in progress or has failed, the results
    reflect the current job status.
    """

    scanID: str = None
    results: List[RemediationResult] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "AiRemediationDetails":
        return cls(
            scanID=item.get("scanID"),
            results=[RemediationResult.from_dict(r) for r in item.get("results", [])],
        )
