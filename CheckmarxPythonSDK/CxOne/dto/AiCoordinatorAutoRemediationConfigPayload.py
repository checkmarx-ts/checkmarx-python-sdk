from dataclasses import dataclass
from typing import List, Optional, Union

from .AiCoordinatorScannerType import AiCoordinatorScannerType
from .AiCoordinatorRiskState import AiCoordinatorRiskState
from .AiCoordinatorRiskStatus import AiCoordinatorRiskStatus
from .AiCoordinatorSeverityLevel import AiCoordinatorSeverityLevel


@dataclass
class AiCoordinatorAutoRemediationConfigPayload:
    """Account-scope auto-remediation eligibility filters. Byte-identical
    shape on read and write, like AiCoordinatorAutoTriageConfigPayload.

    risk_aggregation/aggregation_limit: when omitted on write, the stored
    value is left unchanged; absent storage reads back as False/50.
    """
    projects: Optional[List[str]] = None
    branches: Optional[List[str]] = None
    scanner_types: Optional[List[Union[AiCoordinatorScannerType, str]]] = None
    risk_states: Optional[List[Union[AiCoordinatorRiskState, str]]] = None
    risk_statuses: Optional[List[Union[AiCoordinatorRiskStatus, str]]] = None
    severity_levels: Optional[List[Union[AiCoordinatorSeverityLevel, str]]] = None
    risk_aggregation: Optional[bool] = None
    aggregation_limit: Optional[int] = None

    @staticmethod
    def _val(v):
        return v.value if hasattr(v, "value") else v

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorAutoRemediationConfigPayload":
        return cls(
            projects=item.get("projects"),
            branches=item.get("branches"),
            scanner_types=item.get("scannerTypes"),
            risk_states=item.get("riskStates"),
            risk_statuses=item.get("riskStatuses"),
            severity_levels=item.get("severityLevels"),
            risk_aggregation=item.get("riskAggregation"),
            aggregation_limit=item.get("aggregationLimit"),
        )

    def to_dict(self) -> dict:
        raw = {
            "projects": self.projects,
            "branches": self.branches,
            "scannerTypes": (
                [self._val(v) for v in self.scanner_types]
                if self.scanner_types is not None else None
            ),
            "riskStates": (
                [self._val(v) for v in self.risk_states]
                if self.risk_states is not None else None
            ),
            "riskStatuses": (
                [self._val(v) for v in self.risk_statuses]
                if self.risk_statuses is not None else None
            ),
            "severityLevels": (
                [self._val(v) for v in self.severity_levels]
                if self.severity_levels is not None else None
            ),
            "riskAggregation": self.risk_aggregation,
            "aggregationLimit": self.aggregation_limit,
        }
        return {k: v for k, v in raw.items() if v is not None}
