from dataclasses import dataclass


@dataclass
class CloudInsightEnrichAccount:
    name: str = None
    account_id: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "CloudInsightEnrichAccount":
        return cls(
            name=item.get("name"),
            account_id=item.get("accountID"),
        )
