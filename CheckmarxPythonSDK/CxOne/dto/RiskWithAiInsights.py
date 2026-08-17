from dataclasses import dataclass
from typing import Optional

from .AiTriageInsight import AiTriageInsight
from .RemediationInsight import RemediationInsight


@dataclass
class RiskWithAiInsights:
    """A risk with AI triage and remediation data from GET /api/risks/ai-insights.

    Attributes:
        id (str): Risk identifier (result hash).
        riskName (str): Name of the vulnerability query.
        status (str): NEW, RECURRENT, or FIXED.
        state (str): TO_VERIFY, NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE,
            CONFIRMED, or URGENT.
        severity (str): CRITICAL, HIGH, MEDIUM, LOW, or INFO.
        firstDetectionDate (str): RFC3339 datetime of first detection.
        origin (str): Scan origin (e.g. webapp, PR Webhook).
        source (str): Source SCM provider (e.g. github).
        assetName (str): Name of the affected asset (e.g. file path).
        subAssetName (str): Sub-asset name (e.g. method name).
        projectId (str): Project UUID.
        scanId (str): Scan UUID.
        engine (str): Scanner engine: SAST, IAC, or SCA.
        groupId (str): Vulnerability group identifier (similarityId).
        assetType (str): ENDPOINT, SOURCE_CODE, CONTAINER_IMAGE,
            MANIFEST_FILE, or XML_FILE.
        aiTriage (AiTriageInsight or None): AI triage summary if available.
        remediation (RemediationInsight or None): Remediation summary if
            available.
    """

    id: Optional[str] = None
    riskName: Optional[str] = None
    status: Optional[str] = None
    state: Optional[str] = None
    severity: Optional[str] = None
    firstDetectionDate: Optional[str] = None
    origin: Optional[str] = None
    source: Optional[str] = None
    assetName: Optional[str] = None
    subAssetName: Optional[str] = None
    projectId: Optional[str] = None
    scanId: Optional[str] = None
    engine: Optional[str] = None
    groupId: Optional[str] = None
    assetType: Optional[str] = None
    aiTriage: Optional[AiTriageInsight] = None
    remediation: Optional[RemediationInsight] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RiskWithAiInsights":
        return cls(
            id=item.get("id"),
            riskName=item.get("riskName"),
            status=item.get("status"),
            state=item.get("state"),
            severity=item.get("severity"),
            firstDetectionDate=item.get("firstDetectionDate"),
            origin=item.get("origin"),
            source=item.get("source"),
            assetName=item.get("assetName"),
            subAssetName=item.get("subAssetName"),
            projectId=item.get("projectId"),
            scanId=item.get("scanId"),
            engine=item.get("engine"),
            groupId=item.get("groupId"),
            assetType=item.get("assetType"),
            aiTriage=(
                AiTriageInsight.from_dict(item["aiTriage"])
                if item.get("aiTriage")
                else None
            ),
            remediation=(
                RemediationInsight.from_dict(item["remediation"])
                if item.get("remediation")
                else None
            ),
        )
