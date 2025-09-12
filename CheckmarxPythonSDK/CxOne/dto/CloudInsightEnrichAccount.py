from dataclasses import dataclass


@dataclass
class CloudInsightEnrichAccount:
    name: str = None  # The account name
    account_id: str = None  # A unique identifier to the enrichment account


def construct_cloud_insight_enrich_account(item):
    return CloudInsightEnrichAccount(
            name=item.get("name"),
            account_id=item.get("accountID"),
        )
