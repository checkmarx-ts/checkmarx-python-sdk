from dataclasses import dataclass
from typing import List, Optional, Union

from .AiCoordinatorScannerType import AiCoordinatorScannerType
from .AiCoordinatorRiskStatus import AiCoordinatorRiskStatus
from .AiCoordinatorSeverityLevel import AiCoordinatorSeverityLevel


@dataclass
class AiCoordinatorAutoTriageConfigPayload:
    """Account-scope auto-triage eligibility filters.

    Byte-identical shape on read (nested under
    AiCoordinatorAutoTriageAccountConfigItem.config) and on write (nested
    under AiCoordinatorAutoTriageAccountConfigWriteItem.config) -- the spec
    only differs in minItems validation, which isn't visible client-side --
    so this one dataclass serves both directions.
    """
    projects: Optional[List[str]] = None
    branches: Optional[List[str]] = None
    scanner_types: Optional[List[Union[AiCoordinatorScannerType, str]]] = None
    risk_statuses: Optional[List[Union[AiCoordinatorRiskStatus, str]]] = None
    severity_levels: Optional[List[Union[AiCoordinatorSeverityLevel, str]]] = None

    @staticmethod
    def _val(v):
        return v.value if hasattr(v, "value") else v

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorAutoTriageConfigPayload":
        return cls(
            projects=item.get("projects"),
            branches=item.get("branches"),
            scanner_types=item.get("scannerTypes"),
            risk_statuses=item.get("riskStatuses"),
            severity_levels=item.get("severityLevels"),
        )

    def to_dict(self) -> dict:
        raw = {
            "projects": self.projects,
            "branches": self.branches,
            "scannerTypes": (
                [self._val(v) for v in self.scanner_types]
                if self.scanner_types is not None else None
            ),
            "riskStatuses": (
                [self._val(v) for v in self.risk_statuses]
                if self.risk_statuses is not None else None
            ),
            "severityLevels": (
                [self._val(v) for v in self.severity_levels]
                if self.severity_levels is not None else None
            ),
        }
        return {k: v for k, v in raw.items() if v is not None}
