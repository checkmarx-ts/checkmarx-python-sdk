from dataclasses import dataclass


@dataclass
class AuditQuery:
    id: str = None
    source: str = None

    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
        }
