from dataclasses import dataclass
from .ContributorScmInsights import ContributorScmInsights


@dataclass
class ContributorInsights:
    total: int = None
    max: int = None
    github: ContributorScmInsights = None
    gitlab: ContributorScmInsights = None
    azure: ContributorScmInsights = None
    bitbucket: ContributorScmInsights = None
    other: ContributorScmInsights = None

    @classmethod
    def from_dict(cls, item: dict) -> "ContributorInsights":
        return cls(
            total=item.get("total"),
            max=item.get("max"),
            github=ContributorScmInsights.from_dict(item["github"]) if item.get("github") else None,
            gitlab=ContributorScmInsights.from_dict(item["gitlab"]) if item.get("gitlab") else None,
            azure=ContributorScmInsights.from_dict(item["azure"]) if item.get("azure") else None,
            bitbucket=ContributorScmInsights.from_dict(item["bitbucket"]) if item.get("bitbucket") else None,
            other=ContributorScmInsights.from_dict(item["other"]) if item.get("other") else None,
        )
