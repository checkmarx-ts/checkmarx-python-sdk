from dataclasses import dataclass, field
from typing import List

from .ScaRegistryConfiguration import ScaRegistryConfiguration


@dataclass
class ScaProjectWithConfigurations:
    """A project with its associated private registry configurations.

    Attributes:
        id (str): Unique identifier of the project.
        tenantId (str): ID of the tenant account associated with this project.
        configurations (List[ScaRegistryConfiguration]): Configurations
            associated with this project.
    """

    id: str = None
    tenantId: str = None
    configurations: List[ScaRegistryConfiguration] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "ScaProjectWithConfigurations":
        return cls(
            id=item.get("id"),
            tenantId=item.get("tenantId"),
            configurations=[
                ScaRegistryConfiguration.from_dict(c)
                for c in item.get("configurations", [])
            ],
        )
