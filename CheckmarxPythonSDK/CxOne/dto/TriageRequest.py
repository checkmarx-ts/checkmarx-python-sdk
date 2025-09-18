from dataclasses import dataclass


@dataclass
class TriageRequest:
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


def construct_triage_request(item):
    return TriageRequest(
        result_id=item.get("resultId"),
        project_id=item.get("projectId"),
        state=item.get("state"),
        severity=item.get("severity"),
    )
