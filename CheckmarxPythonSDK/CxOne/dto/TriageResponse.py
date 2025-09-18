from dataclasses import dataclass


@dataclass
class TriageResponse:
    result_id: str = None
    project_id: str = None
    state: str = None
    severity: str = None

    def to_dict(self):
        return {
            "resultId": self.result_id,
            "projectId": self.project_id,
            "state": self.state,
            "severity": self.severity
        }


def construct_triage_response(item):
    return TriageResponse(
        result_id=item.get("resultId"),
        project_id=item.get("projectId"),
        state=item.get("state"),
        severity=item.get("severity"),
    )
