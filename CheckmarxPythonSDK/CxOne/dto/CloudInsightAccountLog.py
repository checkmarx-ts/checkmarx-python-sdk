from dataclasses import dataclass


@dataclass
class CloudInsightAccountLog:
    id: str = None
    event_type: str = None
    description: str = None
    details: str = None
    tenant_id: str = None
    account_id: str = None
    status: str = None
    sync_id: str = None
    created_at: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "CloudInsightAccountLog":
        return cls(
            id=item.get("id"),
            event_type=item.get("eventType"),
            description=item.get("description"),
            details=item.get("details"),
            tenant_id=item.get("tenantId"),
            account_id=item.get("accountId"),
            status=item.get("status"),
            sync_id=item.get("syncId"),
            created_at=item.get("createdAt"),
        )
