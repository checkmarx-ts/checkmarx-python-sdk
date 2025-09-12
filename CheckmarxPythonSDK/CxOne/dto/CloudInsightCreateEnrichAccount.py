from dataclasses import dataclass


@dataclass
class CloudInsightCreateEnrichAccount:
    name: str = None  # The account name
    external_id: str = None  # A unique identifier provided by Checkmarx

    def to_dict(self):
        return {
                "name": self.name,
                "externalID": self.external_id
            }
