from dataclasses import dataclass


@dataclass
class Rule:
    """
    Attributes:
        id (str): uuid
        type (str): example: project.tag.key-value.exists
        value (str): example: key;value
    """

    id: str
    type: str
    value: str

    @classmethod
    def from_dict(cls, item: dict) -> "Rule":
        return cls(
            id=item.get("id"),
            type=item.get("type"),
            value=item.get("value"),
        )
