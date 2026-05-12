from dataclasses import dataclass
from .LogItem import LogItem
from typing import List


@dataclass
class ImportItemWithLogs:
    migration_id: str = None
    status: str = None
    created_at: str = None
    logs: List[LogItem] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ImportItemWithLogs":
        return cls(
            migration_id=item.get("migrationId"),
            status=item.get("status"),
            created_at=item.get("createdAt"),
            logs=[LogItem.from_dict(log) for log in (item.get("logs") or [])],
        )
