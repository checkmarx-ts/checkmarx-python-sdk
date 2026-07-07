from dataclasses import dataclass, field, asdict
from typing import List

from .SupplyChainRiskAction import SupplyChainRiskAction


@dataclass
class BulkSupplyChainRiskEntry:
    """A single supply chain risk entry within a bulk update request.

    Attributes:
        packageName (str): The name of the package.
        packageVersion (str): The version of the package.
        packageManager (str): The package manager used.
        supplyChainRiskId (str): The supply chain risk identifier.
        projectIds (List[str]): The project identifiers.
    """

    packageName: str
    packageVersion: str
    packageManager: str
    supplyChainRiskId: str
    projectIds: List[str] = field(default_factory=list)

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class UpdateSupplyChainRisksBulkRequest:
    """Request body for POST
    /api/sca/management-of-risk/package-supply-chain-risks/bulk.

    Attributes:
        packageSupplyChainRisks (List[BulkSupplyChainRiskEntry]): Collection
            of supply chain risks to change.
        actions (List[SupplyChainRiskAction]): Shared actions to apply to all
            specified risks.
    """

    packageSupplyChainRisks: List[BulkSupplyChainRiskEntry] = field(
        default_factory=list
    )
    actions: List[SupplyChainRiskAction] = field(default_factory=list)
