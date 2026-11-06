from dataclasses import dataclass
from typing import Optional


@dataclass
class IncidentResultWebDTO:
    """A single result underlying a policy incident.

    Attributes:
        id (Optional[int]): Result ID.
        severity (Optional[str]): Result severity.
        issue (Optional[str]): Issue/query name.
        issueLink (Optional[str]): Link to the issue in the CxOne UI.
        cweLink (Optional[str]): Link to the CWE reference.
        sourceFilePackage (Optional[str]): Source file or package name.
        sourceFileLink (Optional[str]): Link to the source file in the CxOne UI.
        lineNumber (Optional[int]): Line number of the finding.
        insight (Optional[str]): Remediation insight text.
        insightLink (Optional[str]): Link to the remediation insight.
        resultId (Optional[str]): The underlying result's ID.
        recommendedVersion (Optional[str]): Recommended package version (SCA).
        attackVector (Optional[str]): Attack vector description.
        attackComplexity (Optional[str]): Attack complexity description.
        riskOrchestrationLink (Optional[str]): Link to Risk Orchestration.
        sastResultsLink (Optional[str]): Link to the SAST result.
    """

    id: Optional[int] = None
    severity: Optional[str] = None
    issue: Optional[str] = None
    issueLink: Optional[str] = None
    cweLink: Optional[str] = None
    sourceFilePackage: Optional[str] = None
    sourceFileLink: Optional[str] = None
    lineNumber: Optional[int] = None
    insight: Optional[str] = None
    insightLink: Optional[str] = None
    resultId: Optional[str] = None
    recommendedVersion: Optional[str] = None
    attackVector: Optional[str] = None
    attackComplexity: Optional[str] = None
    riskOrchestrationLink: Optional[str] = None
    sastResultsLink: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "IncidentResultWebDTO":
        return cls(
            id=item.get("id"),
            severity=item.get("severity"),
            issue=item.get("issue"),
            issueLink=item.get("issueLink"),
            cweLink=item.get("cweLink"),
            sourceFilePackage=item.get("sourceFilePackage"),
            sourceFileLink=item.get("sourceFileLink"),
            lineNumber=item.get("lineNumber"),
            insight=item.get("insight"),
            insightLink=item.get("insightLink"),
            resultId=item.get("resultId"),
            recommendedVersion=item.get("recommendedVersion"),
            attackVector=item.get("attackVector"),
            attackComplexity=item.get("attackComplexity"),
            riskOrchestrationLink=item.get("riskOrchestrationLink"),
            sastResultsLink=item.get("sastResultsLink"),
        )
