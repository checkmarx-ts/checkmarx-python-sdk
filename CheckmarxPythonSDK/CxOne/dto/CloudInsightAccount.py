from dataclasses import dataclass


@dataclass
class CloudInsightAccount:
    id: str = None  # A unique identifier for an account
    name: str = None  # The account name
    credentials: dict = None  # The account credentials to connect to the provider
    account_type: int = None  # The type of account
    tenant_id: str = None  # The tenantId where the account belongs to
    created_at: str = None
    updated_at: str = None
    last_scan_date: str = None
    next_scan_date: str = None


def construct_cloud_insight_account(item):
    return CloudInsightAccount(
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
