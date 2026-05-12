from dataclasses import dataclass


@dataclass
class TaskInfo:
    source: str = None
    timestamp: str = None
    info: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "TaskInfo":
        return cls(
            source=item.get("source"),
            timestamp=item.get("timestamp"),
            info=item.get("info"),
        )
