from dataclasses import dataclass
from typing import Optional


@dataclass
class AiCoordinatorAutoTriageAllowOverridePayload:
    """Account-scope allowOverride flags for auto-triage -- which config
    fields a project is allowed to override. Write-only (the account
    GET response's allowOverride is an unstructured bool map instead).
    All default False server-side when omitted.
    """
    projects: Optional[bool] = None
    branches: Optional[bool] = None
    scanner_types: Optional[bool] = None
    risk_statuses: Optional[bool] = None
    severity_levels: Optional[bool] = None

    def to_dict(self) -> dict:
        raw = {
            "projects": self.projects,
            "branches": self.branches,
            "scannerTypes": self.scanner_types,
            "riskStatuses": self.risk_statuses,
            "severityLevels": self.severity_levels,
        }
        return {k: v for k, v in raw.items() if v is not None}
