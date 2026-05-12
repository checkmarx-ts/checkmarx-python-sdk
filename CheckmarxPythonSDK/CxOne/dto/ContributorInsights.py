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
            github=ContributorScmInsights.from_dict(item.get("github")),
            gitlab=ContributorScmInsights.from_dict(item.get("gitlab")),
            azure=ContributorScmInsights.from_dict(item.get("azure")),
            bitbucket=ContributorScmInsights.from_dict(item.get("bitbucket")),
            other=ContributorScmInsights.from_dict(item.get("other")),
        )
