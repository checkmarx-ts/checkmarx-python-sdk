from dataclasses import dataclass


@dataclass
class CloudInsightCreateEnrichAccount:
    name: str = None  # The account name
    externalID: str = None  # A unique identifier provided by Checkmarx
