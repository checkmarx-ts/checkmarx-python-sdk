from dataclasses import dataclass, field
from typing import List


@dataclass
class ScaRegistryConfiguration:
    """A private registry configuration for SCA.

    Attributes:
        id (str): Unique identifier of this configuration.
        configurationName (str): Name of this configuration.
        tenantId (str): ID of the tenant account associated with this
            configuration.
        content (str): The content of this configuration (e.g. XML for NuGet
            config, JSON for npmrc).
        tags (List[dict]): Tags assigned to this configuration.
        packageManager (str): The package manager of registry associated with
            this configuration.
        projects (List[dict]): The projects associated with this configuration.
        lastUpdate (str): Last update of this configuration. ISO-8601 timestamp
            in UTC.
    """

    id: str = None
    configurationName: str = None
    tenantId: str = None
    content: str = None
    tags: List[dict] = field(default_factory=list)
    packageManager: str = None
    projects: List[dict] = field(default_factory=list)
    lastUpdate: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScaRegistryConfiguration":
        return cls(
            id=item.get("id"),
            configurationName=item.get("configurationName"),
            tenantId=item.get("tenantId"),
            content=item.get("content"),
            tags=item.get("tags", []),
            packageManager=item.get("packageManager"),
            projects=item.get("projects", []),
            lastUpdate=item.get("lastUpdate"),
        )
