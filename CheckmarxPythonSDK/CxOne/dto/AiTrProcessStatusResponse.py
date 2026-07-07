from dataclasses import dataclass, field
from typing import List

from .AiTrProcessResult import AiTrProcessResult


@dataclass
class AiTrProcessStatusResponse:
    """Response from GET /api/v1/ai-tr/process/{processId}.

    Attributes:
        processId (str): Unique identifier of the triggered AI Triage or AI
            Remediation process.
        status (str): Overall status of the triggered process batch. Allowed
            values: 'in_progress', 'completed', 'completed_with_errors',
            'failed'.
        results (List[AiTrProcessResult]): Per-vulnerability status results.
    """

    processId: str = None
    status: str = None
    results: List[AiTrProcessResult] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "AiTrProcessStatusResponse":
        return cls(
            processId=item.get("processId"),
            status=item.get("status"),
            results=[
                AiTrProcessResult.from_dict(r)
                for r in item.get("results", [])
            ],
        )
