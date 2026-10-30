from dataclasses import dataclass, field
from typing import List, Optional, Union

from .AiCoordinatorAutoTriageProjectConfigItem import AiCoordinatorAutoTriageProjectConfigItem
from .AiCoordinatorAutoRemediationProjectConfigItem import AiCoordinatorAutoRemediationProjectConfigItem


@dataclass
class AiCoordinatorProjectConfigResponse:
    """Response from GET/PUT /projects/{project_id}/configuration.

    `configurations` is a discriminated union on the `feature` field
    (auto_triage / auto_remediation); any other/future feature value is
    kept as a raw dict rather than dropped.
    """
    scope: str = "project"
    project_id: Optional[str] = None
    configurations: List[
        Union[
            AiCoordinatorAutoTriageProjectConfigItem,
            AiCoordinatorAutoRemediationProjectConfigItem,
            dict,
        ]
    ] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorProjectConfigResponse":
        configurations = []
        for c in item.get("configurations") or []:
            feature = c.get("feature")
            if feature == "auto_triage":
                configurations.append(
                    AiCoordinatorAutoTriageProjectConfigItem.from_dict(c)
                )
            elif feature == "auto_remediation":
                configurations.append(
                    AiCoordinatorAutoRemediationProjectConfigItem.from_dict(c)
                )
            else:
                configurations.append(c)
        return cls(
            scope=item.get("scope", "project"),
            project_id=item.get("projectId"),
            configurations=configurations,
        )
