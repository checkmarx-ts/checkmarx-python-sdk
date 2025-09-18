from dataclasses import dataclass


@dataclass
class ScmOrganization:
    """

    Args:
        org_identity (str): The name of the organization that you are importing from. Note: Each API call can only
            import repos from a single organization.
        monitor_for_new_projects (bool): If true, then after the initial configuration, whenever a new repo is
            created in the organization, a corresponding project will be created in Checkmarx.
    """

    org_identity: str
    monitor_for_new_projects: bool

    def to_dict(self):
        return {
            "orgIdentity": self.org_identity,
            "monitorForNewProjects": self.monitor_for_new_projects
        }
