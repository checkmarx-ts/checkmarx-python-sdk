from dataclasses import dataclass


@dataclass
class ContributorScmInsights:
    project_count: int = None
    contributor_count: int = None


def construct_contributor_scm_insights(item):
    return ContributorScmInsights(
        project_count=item.get("projectCount"),
        contributor_count=item.get("contributorCount"),
    )
