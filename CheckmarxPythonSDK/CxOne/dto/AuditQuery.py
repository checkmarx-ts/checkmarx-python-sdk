from dataclasses import dataclass


@dataclass
class AuditQuery:
    id: str = None
    source: str = None
