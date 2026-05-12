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

    @classmethod
    def from_dict(cls, item: dict) -> "Contributors":
        return cls(
            allowed_contributors=item.get("allowedContributors"),
            current_contributors=item.get("currentContributors"),
        )
