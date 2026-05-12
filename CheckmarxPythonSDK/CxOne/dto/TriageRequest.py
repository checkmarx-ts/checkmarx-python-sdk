from dataclasses import dataclass


@dataclass
class TriageRequest:
    resultId: str = None
    projectId: str = None
    state: str = None
    severity: str = None
