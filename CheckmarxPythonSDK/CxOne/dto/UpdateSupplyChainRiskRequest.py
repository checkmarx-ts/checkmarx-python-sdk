from dataclasses import dataclass, field, asdict
from typing import List

from .SupplyChainRiskAction import SupplyChainRiskAction


@dataclass
class UpdateSupplyChainRiskRequest:
    """Request body for POST
    /api/sca/management-of-risk/package-supply-chain-risks.

    Attributes:
        packageName (str): The name of the package.
        packageVersion (str): The version of the package.
        packageManager (str): The package manager used.
        supplyChainRiskId (str): The supply chain risk ID to change.
        projectIds (List[str]): List of project IDs associated with the risk.
        actions (List[SupplyChainRiskAction]): Actions to perform (ChangeState
            and/or ChangeScore).
    """

    packageName: str
    packageVersion: str
    packageManager: str
    supplyChainRiskId: str
    projectIds: List[str] = field(default_factory=list)
    actions: List[SupplyChainRiskAction] = field(default_factory=list)

    def to_dict(self):
        return {
            k: v
            for k, v in asdict(self).items()
            if v is not None
        }
