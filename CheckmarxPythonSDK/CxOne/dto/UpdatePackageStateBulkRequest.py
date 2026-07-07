from dataclasses import dataclass, field, asdict
from typing import List

from .PackageAction import PackageAction


@dataclass
class BulkPackageEntry:
    """A single package entry within a bulk update request.

    Attributes:
        packageName (str): The name of the package.
        packageVersion (str): The version of the package.
        packageManager (str): The package manager used.
        projectId (str): The project ID for which the change is being made.
    """

    packageName: str
    packageVersion: str
    packageManager: str
    projectId: str

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class UpdatePackageStateBulkRequest:
    """Request body for POST /api/sca/management-of-risk/packages/bulk.

    Attributes:
        packagesProfile (List[BulkPackageEntry]): List of packages to update,
            each with its own projectId.
        actions (List[PackageAction]): List of actions to apply to all
            specified packages.
    """

    packagesProfile: List[BulkPackageEntry] = field(default_factory=list)
    actions: List[PackageAction] = field(default_factory=list)
