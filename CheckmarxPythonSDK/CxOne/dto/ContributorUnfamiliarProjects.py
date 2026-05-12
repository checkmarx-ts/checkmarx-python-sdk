from dataclasses import dataclass


@dataclass
class ContributorUnfamiliarProjects:
    unfamiliar_projects: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "ContributorUnfamiliarProjects":
        return cls(unfamiliar_projects=item.get("unfamiliarProjects"))
