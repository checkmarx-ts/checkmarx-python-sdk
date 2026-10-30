from dataclasses import dataclass, field
from typing import List, Optional

from .ViolatedPolicyWebDto import ViolatedPolicyWebDto


@dataclass
class PolicyViolationWebDto:
    """Response from GET /api/policy_management_service_uri/policy_violations.

    Attributes:
        scanId (Optional[str]): The scan's UUID.
        projectId (Optional[str]): The project ID.
        generatedOn (Optional[str]): When the evaluation was generated (date-time).
        policies (List[ViolatedPolicyWebDto]): Policies violated by the scan.
        status (Optional[str]): Evaluation status. Values: COMPLETED, EVALUATING, NONE.
    """

    scanId: Optional[str] = None
    projectId: Optional[str] = None
    generatedOn: Optional[str] = None
    policies: List[ViolatedPolicyWebDto] = field(default_factory=list)
    status: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "PolicyViolationWebDto":
        return cls(
            scanId=item.get("scanId"),
            projectId=item.get("projectId"),
            generatedOn=item.get("generatedOn"),
            policies=[
                ViolatedPolicyWebDto.from_dict(p)
                for p in (item.get("policies") or [])
            ],
            status=item.get("status"),
        )
