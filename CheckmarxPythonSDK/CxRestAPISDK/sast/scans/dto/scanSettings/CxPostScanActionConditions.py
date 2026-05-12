from dataclasses import dataclass
from typing import Optional


@dataclass
class CxPostScanActionConditions:

    run_only_when_new_results: Optional[bool] = None
    run_only_when_new_results_min_severity: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxPostScanActionConditions":
        return cls(
            run_only_when_new_results=item.get("runOnlyWhenNewResults"),
            run_only_when_new_results_min_severity=item.get(
                "runOnlyWhenNewResultsMinSeverity"
            ),
        )
