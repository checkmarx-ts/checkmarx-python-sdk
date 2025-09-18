from dataclasses import dataclass


@dataclass
class Contributors:
    """

    Attributes:
        allowed_contributors (int):
        current_contributors (int):
    """

    allowed_contributors: int
    current_contributors: int


def construct_contributors(item):
    return Contributors(
        allowed_contributors=item.get("allowedContributors"),
        current_contributors=item.get("currentContributors")
    )
