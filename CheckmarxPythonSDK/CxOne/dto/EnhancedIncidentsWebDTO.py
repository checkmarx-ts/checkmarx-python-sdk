from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EnhancedIncidentsWebDTO:
    """A policy incident, as returned by the enhanced (v2) incidents endpoint.

    Same shape as IncidentWebDto plus the originating scanner engine.

    Attributes:
        id (Optional[int]): Incident ID.
        policyName (Optional[str]): Name of the violated policy.
        projectName (Optional[str]): Name of the project scanned.
        branch (Optional[str]): Branch scanned.
        ruleName (Optional[str]): Name of the violated rule.
        scanId (Optional[str]): The scan's UUID.
        scanDate (Optional[str]): When the scan ran (date-time).
        policyTags (List[str]): Tags on the violated policy.
        defaultPolicy (Optional[bool]): Whether the policy is the tenant default.
        defaultPolicyEvaluation (Optional[bool]): Whether the default policy
            was the one evaluated.
        engine (Optional[str]): The scanner engine that produced the incident.
    """

    id: Optional[int] = None
    policyName: Optional[str] = None
    projectName: Optional[str] = None
    branch: Optional[str] = None
    ruleName: Optional[str] = None
    scanId: Optional[str] = None
    scanDate: Optional[str] = None
    policyTags: List[str] = field(default_factory=list)
    defaultPolicy: Optional[bool] = None
    defaultPolicyEvaluation: Optional[bool] = None
    engine: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "EnhancedIncidentsWebDTO":
        return cls(
            id=item.get("id"),
            policyName=item.get("policyName"),
            projectName=item.get("projectName"),
            branch=item.get("branch"),
            ruleName=item.get("ruleName"),
            scanId=item.get("scanId"),
            scanDate=item.get("scanDate"),
            policyTags=list(item.get("policyTags") or []),
            defaultPolicy=item.get("defaultPolicy"),
            defaultPolicyEvaluation=item.get("defaultPolicyEvaluation"),
            engine=item.get("engine"),
        )
