from dataclasses import dataclass


@dataclass
class ImportItem:
    """

    Args:
        migration_id (str):
        status (str): pending, running, completed, failed
        created_at (str):
    """
    migration_id: str
    status: str
    created_at: str


def construct_import_item(item):
    return ImportItem(
        migration_id=item.get("migrationId"),
        status=item.get("status"),
        created_at=item.get("createdAt")
    )
