from dataclasses import dataclass
from .ContributorScmInsights import ContributorScmInsights, construct_contributor_scm_insights


@dataclass
class ContributorInsights:
    total: int = None
    max: int = None
    github: ContributorScmInsights = None
    gitlab: ContributorScmInsights = None
    azure: ContributorScmInsights = None
    bitbucket: ContributorScmInsights = None
    other: ContributorScmInsights = None


def construct_contributor_insights(item):
    return ContributorInsights(
        total=item.get("total"),
        max=item.get("max"),
        github=construct_contributor_scm_insights(item.get("github")),
        gitlab=construct_contributor_scm_insights(item.get("gitlab")),
        azure=construct_contributor_scm_insights(item.get("azure")),
        bitbucket=construct_contributor_scm_insights(item.get("bitbucket")),
        other=construct_contributor_scm_insights(item.get("other")),
    )
