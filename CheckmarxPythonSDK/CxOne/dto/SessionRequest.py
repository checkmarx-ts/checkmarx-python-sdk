from dataclasses import dataclass


@dataclass
class SessionRequest:
    projectId: str
    scanId: str
    scanner: str = "sast"
    timeout: int = None
    uploadUrl: str = None
