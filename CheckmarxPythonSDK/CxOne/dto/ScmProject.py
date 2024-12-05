from typing import List
from .ProjectSettings import ProjectSettings


class ScmProject(object):

    def __init__(self,
                 scm_repository_url: str,
                 protected_branches: List[str] = None,
                 branch_to_scan_upon_creation: str = None,
                 custom_settings: ProjectSettings = None,
                 ssh_key: str = None
                 ):
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
        self.scmRepositoryUrl = scm_repository_url
        self.protectedBranches = protected_branches
        self.sshKey = ssh_key
        self.branchToScanUponCreation = branch_to_scan_upon_creation
        self.customSettings = custom_settings

    def __str__(self):
        return (f"ScmProject( scmRepositoryUrl={self.scmRepositoryUrl}, "
                f"protectedBranches={self.protectedBranches}, "
                f"sshKey={self.sshKey}, "
                f"branchToScanUponCreation={self.branchToScanUponCreation}, "
                f"customSettings={self.customSettings}"
                f")")

    def to_dict(self):
        result = {"scmRepositoryUrl": self.scmRepositoryUrl}
        if self.protectedBranches is not None:
            result.update({"protectedBranches": self.protectedBranches})
        if self.sshKey is not None:
            result.update({"sshKey": self.sshKey})
        if self.branchToScanUponCreation is not None:
            result.update({"branchToScanUponCreation": self.branchToScanUponCreation})
        if self.customSettings is not None:
            result.update({"customSettings": self.customSettings.to_dict()})
        return result
