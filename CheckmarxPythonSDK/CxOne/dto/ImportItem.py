from dataclasses import dataclass


@dataclass
class ImportItem:
    migration_id: str = None
    status: str = None
    created_at: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "ImportItem":
        return cls(
            migration_id=item.get("migrationId"),
            status=item.get("status"),
            created_at=item.get("createdAt"),
        )
