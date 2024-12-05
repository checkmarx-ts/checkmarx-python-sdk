class ScmOrganization(object):

    def __init__(self,
                 org_identity: str,
                 monitor_for_new_projects: bool
                 ):
        """

        Args:
            org_identity (str): The name of the organization that you are importing from. Note: Each API call can only
                import repos from a single organization.
            monitor_for_new_projects (bool): If true, then after the initial configuration, whenever a new repo is
                created in the organization, a corresponding project will be created in Checkmarx.
        """
        self.orgIdentity = org_identity
        self.monitorForNewProjects = monitor_for_new_projects

    def __str__(self):
        return f"ScmOrganization(orgIdentity={self.orgIdentity}, monitorForNewProjects={self.monitorForNewProjects})"

    def to_dict(self):
        return {
            "orgIdentity": self.orgIdentity,
            "monitorForNewProjects": self.monitorForNewProjects
        }
