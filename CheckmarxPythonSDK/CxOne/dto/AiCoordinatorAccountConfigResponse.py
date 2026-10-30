from dataclasses import dataclass, field
from typing import List, Union

from .AiCoordinatorAutoTriageAccountConfigItem import AiCoordinatorAutoTriageAccountConfigItem
from .AiCoordinatorAutoRemediationAccountConfigItem import AiCoordinatorAutoRemediationAccountConfigItem


@dataclass
class AiCoordinatorAccountConfigResponse:
    """Response from GET/PUT /configuration.

    `configurations` is a discriminated union on the `feature` field
    (auto_triage / auto_remediation); any other/future feature value is
    kept as a raw dict rather than dropped.
    """
    scope: str = "account"
    configurations: List[
        Union[
            AiCoordinatorAutoTriageAccountConfigItem,
            AiCoordinatorAutoRemediationAccountConfigItem,
            dict,
        ]
    ] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "AiCoordinatorAccountConfigResponse":
        configurations = []
        for c in item.get("configurations") or []:
            feature = c.get("feature")
            if feature == "auto_triage":
                configurations.append(
                    AiCoordinatorAutoTriageAccountConfigItem.from_dict(c)
                )
            elif feature == "auto_remediation":
                configurations.append(
                    AiCoordinatorAutoRemediationAccountConfigItem.from_dict(c)
                )
            else:
                configurations.append(c)
        return cls(
            scope=item.get("scope", "account"),
            configurations=configurations,
        )
