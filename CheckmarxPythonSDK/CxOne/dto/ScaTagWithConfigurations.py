from dataclasses import dataclass, field
from typing import List

from .ScaRegistryConfiguration import ScaRegistryConfiguration


@dataclass
class ScaTagWithConfigurations:
    """A tag with its associated configurations.

    Attributes:
        id (str): Unique identifier of the tag.
        tenantId (str): Unique identifier of the tenant account associated
            with this tag.
        name (str): Name of the tag.
        configurations (List[ScaRegistryConfiguration]): Configurations
            associated with this tag.
    """

    id: str = None
    tenantId: str = None
    name: str = None
    configurations: List[ScaRegistryConfiguration] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "ScaTagWithConfigurations":
        return cls(
            id=item.get("id"),
            tenantId=item.get("tenantId"),
            name=item.get("name"),
            configurations=[
                ScaRegistryConfiguration.from_dict(c)
                for c in item.get("configurations", [])
            ],
        )
