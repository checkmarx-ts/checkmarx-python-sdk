from dataclasses import dataclass


@dataclass
class CloudInsightAccount:
    account_id: str  # A unique identifier for an account
    name: str  # The account name
    credentials: dict  # The account credentials to connect to the provider
    account_type: int  # The type of account
    tenant_id: str  # The tenantId where the account belongs to
    created_at: str
    updated_at: str
    last_scan_date: str
    next_scan_date: str


def construct_cloud_insight_account(item):
    return CloudInsightAccount(
            account_id=item.get("id"),
            name=item.get("name"),
            credentials=item.get("credentials"),
            account_type=item.get("accountType"),
            tenant_id=item.get("tenantId"),
            created_at=item.get("createdAt"),
            updated_at=item.get("updatedAt"),
            last_scan_date=item.get("lastScanDate"),
            next_scan_date=item.get("nextScanDate"),
        )
