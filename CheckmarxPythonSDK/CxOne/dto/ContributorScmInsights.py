from dataclasses import dataclass


@dataclass
class ContributorScmInsights:
    project_count: int = None
    contributor_count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "ContributorScmInsights":
        return cls(
            project_count=item.get("projectCount"),
            contributor_count=item.get("contributorCount"),
        )
