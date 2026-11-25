from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ProjectWebDto:
    """A project reference as used by the Policy Manager service.

    Attributes:
        astProjectId (str): The CxOne project ID. Required.
        name (Optional[str]): The project name.
    """

    astProjectId: str
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ProjectWebDto":
        return cls(
            astProjectId=item.get("astProjectId"),
            name=item.get("name"),
        )

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
