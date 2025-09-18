from dataclasses import dataclass


@dataclass
class ContributorUnfamiliarProjects:
    unfamiliar_projects: int  # Number of projects scanned in the last 90 days where contributors couldn't be counted.


def construct_contributor_unfamiliar_projects(item):
    return ContributorUnfamiliarProjects(
        unfamiliar_projects=item.get("unfamiliarProjects")
    )
