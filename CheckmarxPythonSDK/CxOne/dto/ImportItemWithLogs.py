from dataclasses import dataclass
from .LogItem import LogItem, construct_log_item
from typing import List


@dataclass
class ImportItemWithLogs:
    """

    Args:
        migration_id (str):
        status (str): pending, running, completed, failed
        created_at (str):
        logs (list of LogItem):
    """
    migration_id: str
    status: str
    created_at: str
    logs: List[LogItem]


def construct_import_item_with_logs(item):
    return ImportItemWithLogs(
        migration_id=item.get("migrationId"),
        status=item.get("status"),
        created_at=item.get("createdAt"),
        logs=[
            construct_log_item(log_item) for log_item in item.get("logs", [])
        ]
    )
