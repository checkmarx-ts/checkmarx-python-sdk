from dataclasses import dataclass, field, asdict
from typing import List

from .SupplyChainRiskAction import SupplyChainRiskAction


@dataclass
class BulkVulnerabilityEntry:
    """A single vulnerability entry within a bulk update request.

    Attributes:
        packageName (str): The name of the package.
        packageVersion (str): The version of the package.
        packageManager (str): The package manager used.
        vulnerabilityId (str): The vulnerability ID.
        projectIds (List[str]): The project IDs associated with the package.
    """

    packageName: str
    packageVersion: str
    packageManager: str
    vulnerabilityId: str
    projectIds: List[str] = field(default_factory=list)

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class UpdateVulnerabilitiesBulkRequest:
    """Request body for POST
    /api/sca/management-of-risk/package-vulnerabilities/bulk.

    Attributes:
        packageVulnerabilitiesProfile (List[BulkVulnerabilityEntry]):
            List of vulnerabilities to change.
        actions (List[SupplyChainRiskAction]): Shared actions to apply to all
            specified vulnerabilities.
    """

    packageVulnerabilitiesProfile: List[BulkVulnerabilityEntry] = field(
        default_factory=list
    )
    actions: List[SupplyChainRiskAction] = field(default_factory=list)
