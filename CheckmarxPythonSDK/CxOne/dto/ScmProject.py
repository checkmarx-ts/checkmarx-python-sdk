from dataclasses import dataclass
from typing import List
from .ProjectSettings import ProjectSettings


@dataclass
class ScmProject:
    """

    Args:
        scmRepositoryUrl (str): The URL of the repo.
                    Note: Do not include the .git extension at the end of the URL.
                    Note: When using an SSH Key, you have the option to specify the repo address using the git@...
                    format, e.g., git@github:MyOrg/MyRepo.
        protectedBranches (list of str): A list of branches that will be scanned
                    Note: The max. number of protected branches is 3. If no branch is specified then the default
                    branch will be used.
        sshKey (str): The ssh key for accessing the repo.
                    Note: Newline characters in an SSH key must follow JSON convention and be escaped with \n in
                    the request.
        branchToScanUponCreation (str): Specify the branch that will be scanned after the initial import process
                    is completed.
                    Note: This is only relevant if scanProjectsAfterCreation is true.
        customSettings (ProjectSettings):
    """

    scmRepositoryUrl: str
    protectedBranches: List[str] = None
    branchToScanUponCreation: str = None
    customSettings: ProjectSettings = None
    sshKey: str = None
