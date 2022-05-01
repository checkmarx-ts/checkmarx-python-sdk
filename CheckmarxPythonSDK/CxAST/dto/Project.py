# encoding: utf-8
class Project(object):

    def __init__(self, project_id=None, name=None, groups=None, repo_url=None, main_branch=None, origin=None,
                 created_at=None, updated_at=None, tags=None, criticality=3):
        """

        Args:
            project_id (str, optional): A unique identifier for the project. For 'upload' projects, a value must be entered.
                For 'git' projects, this field can be empty and the repository URL will be designated as the project ID.
            name (str): The project name
            groups (list of str): The groups authorized for this project
            repo_url (str): The representative repository URL
            main_branch (str): The Git main branch
            origin (str): The origin of project
            created_at (str):
            updated_at (str)
            tags (dict):
            criticality (int):
                minimum: 1
                maximum: 5
                default: 3
                example: 3
                Criticality level of the project
        """
        self.id = project_id
        self.name = name
        self.groups = groups
        self.repoUrl = repo_url
        self.mainBranch = main_branch
        self.origin = origin
        self.createdAt = created_at
        self.updatedAt = updated_at
        self.tags = tags
        self.criticality = criticality

    def __str__(self):
        return """Project(id={}, tags={})""".format(
            self.id, self.tags
        )

    def as_dict(self):
        data = {}
        if self.id:
            data.update({"id": self.id})
        if self.tags:
            data.update({"tags": self.tags})
        return data
