# encoding: utf-8
class RichProject(object):
    def __init__(self, project_id, name=None, application_ids=None, groups=None,
                 repo_url=None, main_branch=None, origin=None,
                 created_at=None, updated_at=None, tags=None, criticality=3):
        """

        Args:
            project_id (str): A unique identifier for a project
            name (str): The project name
            application_ids (list of str): The applications this project is associated to
            groups (list of str): The groups authorized for this project
            repo_url: The reprosentive repository URL
            main_branch: The Git main branch
            origin: The origin of project
            created_at:
            updated_at:
            tags:
            criticality:
                minimum: 1
                maximum: 5
                default: 3
                example: 3
                Criticality level of the project
        """
        self.id = project_id
        self.name = name
        self.applicationIds = application_ids
        self.groups = groups
        self.repoUrl = repo_url
        self.mainBranch = main_branch
        self.origin = origin
        self.createdAt = created_at
        self.updatedAt = updated_at
        self.tags = tags
        self.criticality = criticality

    def __str__(self):
        return """RichProject(id={}, name={}, applicationIds={}, groups={}, repoUrl={}, mainBranch={}, 
        origin={}, createdAt={}, updatedAt={}, tags={}, criticality={})""".format(
            self.id,
            self.name,
            self.applicationIds,
            self.groups,
            self.repoUrl,
            self.mainBranch,
            self.origin,
            self.createdAt,
            self.updatedAt,
            self.tags,
            self.criticality,
        )
