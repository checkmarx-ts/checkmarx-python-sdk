from dataclasses import dataclass, field, asdict
from typing import List

from .PackageAction import PackageAction


@dataclass
class UpdatePackageStateRequest:
    """Request body for POST /api/sca/management-of-risk/packages.

    Attributes:
        packageName (str): The name of the package.
        packageVersion (str): The version of the package.
        packageManager (str): The package manager used (e.g. 'Npm', 'Nuget',
            'Maven').
        projectId (str): The project ID for which the change is being made.
        actions (List[PackageAction]): List of actions (mute or snooze) to
            apply to the package.
    """

    packageName: str
    packageVersion: str
    packageManager: str
    projectId: str
    actions: List[PackageAction] = field(default_factory=list)

    def to_dict(self):
        return {
            k: v
            for k, v in asdict(
                self,
                dict_factory=lambda obj: {
                    k: v for k, v in obj if v is not None
                },
            ).items()
            if v is not None
        }
