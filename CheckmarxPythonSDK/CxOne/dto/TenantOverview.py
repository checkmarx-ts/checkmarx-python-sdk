from dataclasses import dataclass


@dataclass
class TenantOverview:
    tenant_id: str = None
    environments_count: int = None
    risk_rating: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "TenantOverview":
        return cls(
            tenant_id=item.get("tenantID"),
            environments_count=item.get("environmentsCount"),
            risk_rating=item.get("riskRating"),
        )
