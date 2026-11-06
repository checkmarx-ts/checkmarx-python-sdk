from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class IncidentWebDto:
    """A policy incident (a policy violation recorded for a scan).

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

    @classmethod
    def from_dict(cls, item: dict) -> "IncidentWebDto":
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
        )
