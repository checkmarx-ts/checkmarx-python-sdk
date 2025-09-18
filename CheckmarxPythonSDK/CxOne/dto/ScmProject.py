from dataclasses import dataclass
from typing import List
from .ProjectSettings import ProjectSettings


@dataclass
class ScmProject:
    """

    Args:
        scm_repository_url (str): The URL of the repo.
                    Note: Do not include the .git extension at the end of the URL.
                    Note: When using an SSH Key, you have the option to specify the repo address using the git@...
                    format, e.g., git@github:MyOrg/MyRepo.
        protected_branches (list of str): A list of branches that will be scanned
                    Note: The max. number of protected branches is 3. If no branch is specified then the default
                    branch will be used.
        ssh_key (str): The ssh key for accessing the repo.
                    Note: Newline characters in an SSH key must follow JSON convention and be escaped with \n in
                    the request.
        branch_to_scan_upon_creation (str): Specify the branch that will be scanned after the initial import process
                    is completed.
                    Note: This is only relevant if scanProjectsAfterCreation is true.
        custom_settings (ProjectSettings):
    """

    scm_repository_url: str
    protected_branches: List[str] = None
    branch_to_scan_upon_creation: str = None
    custom_settings: ProjectSettings = None
    ssh_key: str = None

    def to_dict(self):
        result = {"scmRepositoryUrl": self.scm_repository_url}
        if self.protected_branches is not None:
            result.update({"protectedBranches": self.protected_branches})
        if self.ssh_key is not None:
            result.update({"sshKey": self.ssh_key})
        if self.branch_to_scan_upon_creation is not None:
            result.update({"branchToScanUponCreation": self.branch_to_scan_upon_creation})
        if self.custom_settings is not None:
            result.update({"customSettings": self.custom_settings.to_dict()})
        return result
