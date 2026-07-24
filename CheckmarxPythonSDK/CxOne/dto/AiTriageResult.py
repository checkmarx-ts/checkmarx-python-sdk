from dataclasses import dataclass, field
from typing import List, Optional

from .TriageAnalysis import TriageAnalysis
from .VulnerabilityMetadata import VulnerabilityMetadata
from .ReasoningTrace import ReasoningTrace


@dataclass
class AiTriageResult:
    """Response from GET /api/ai-triage/triage/{project_id}/{group_id}.

    triageStatus allowed values:
        NOT_TRIAGED, IN_PROGRESS, FAILED, VULNERABLE,
        PROPOSED_NOT_EXPLOITABLE, UNCERTAIN, RISK_ACCEPTED
    reachabilityStatus allowed values:
        UNSPECIFIED, REACHABLE, NOT_REACHABLE, UNCERTAIN
    exploitabilityStatus allowed values:
        UNSPECIFIED, EXPLOITABLE, NOT_EXPLOITABLE, UNCERTAIN
    attackabilityStatus allowed values:
        UNSPECIFIED, ATTACKABLE, NOT_ATTACKABLE
    """

    resultID: str = None
    scanner: str = None
    triageStatus: str = None
    reachabilityStatus: str = None
    exploitabilityStatus: str = None
    attackabilityStatus: str = None
    summary: str = None
    triagedAt: str = None
    analysis: Optional[TriageAnalysis] = None
    metadata: Optional[VulnerabilityMetadata] = None
    reasoningTrace: Optional[ReasoningTrace] = None
    mockOrigin: bool = False
    groupId: Optional[str] = None
    projectId: Optional[str] = None
    sourceProjectId: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AiTriageResult":
        return cls(
            resultID=item.get("resultID"),
            scanner=item.get("scanner"),
            triageStatus=item.get("triageStatus"),
            reachabilityStatus=item.get("reachabilityStatus"),
            exploitabilityStatus=item.get("exploitabilityStatus"),
            attackabilityStatus=item.get("attackabilityStatus"),
            summary=item.get("summary"),
            triagedAt=item.get("triagedAt"),
            analysis=(
                TriageAnalysis.from_dict(item["analysis"])
                if item.get("analysis")
                else None
            ),
            metadata=(
                VulnerabilityMetadata.from_dict(item["metadata"])
                if item.get("metadata")
                else None
            ),
            reasoningTrace=(
                ReasoningTrace.from_dict(item["reasoningTrace"])
                if item.get("reasoningTrace")
                else None
            ),
            mockOrigin=item.get("mockOrigin", False),
            groupId=item.get("groupId"),
            projectId=item.get("projectId"),
            sourceProjectId=item.get("sourceProjectId"),
        )
