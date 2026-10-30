from dataclasses import dataclass
from typing import Optional


@dataclass
class AiCoordinatorAutoRemediationAllowOverridePayload:
    """Account-scope allowOverride flags for auto-remediation. Write-only
    (the account GET response's allowOverride is an unstructured bool map
    instead). All default False server-side when omitted.
    """
    projects: Optional[bool] = None
    branches: Optional[bool] = None
    scanner_types: Optional[bool] = None
    risk_states: Optional[bool] = None
    risk_statuses: Optional[bool] = None
    severity_levels: Optional[bool] = None
    risk_aggregation: Optional[bool] = None
    aggregation_limit: Optional[bool] = None

    def to_dict(self) -> dict:
        raw = {
            "projects": self.projects,
            "branches": self.branches,
            "scannerTypes": self.scanner_types,
            "riskStates": self.risk_states,
            "riskStatuses": self.risk_statuses,
            "severityLevels": self.severity_levels,
            "riskAggregation": self.risk_aggregation,
            "aggregationLimit": self.aggregation_limit,
        }
        return {k: v for k, v in raw.items() if v is not None}
