from dataclasses import dataclass


@dataclass
class CloudInsightAccount:
    id: str = None
    name: str = None
    credentials: dict = None
    account_type: int = None
    tenant_id: str = None
    created_at: str = None
    updated_at: str = None
    last_scan_date: str = None
    next_scan_date: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "CloudInsightAccount":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            credentials=item.get("credentials"),
            account_type=item.get("accountType"),
            tenant_id=item.get("tenantId"),
            created_at=item.get("createdAt"),
            updated_at=item.get("updatedAt"),
            last_scan_date=item.get("lastScanDate"),
            next_scan_date=item.get("nextScanDate"),
        )
