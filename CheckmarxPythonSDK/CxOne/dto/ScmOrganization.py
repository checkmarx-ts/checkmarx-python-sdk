from dataclasses import dataclass


@dataclass
class ScmOrganization:
    """

    Args:
        orgIdentity (str): The name of the organization that you are importing from. Note: Each API call can only
            import repos from a single organization.
        monitorForNewProjects (bool): If true, then after the initial configuration, whenever a new repo is
            created in the organization, a corresponding project will be created in Checkmarx.
    """

    orgIdentity: str
    monitorForNewProjects: bool
