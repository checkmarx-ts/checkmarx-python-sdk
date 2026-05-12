from dataclasses import dataclass


@dataclass
class TriageResponse:
    result_id: str = None
    project_id: str = None
    state: str = None
    severity: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "TriageResponse":
        return cls(
            result_id=item.get("resultId"),
            project_id=item.get("projectId"),
            state=item.get("state"),
            severity=item.get("severity"),
        )
