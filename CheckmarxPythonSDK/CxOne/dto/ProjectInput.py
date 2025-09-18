from dataclasses import dataclass
from typing import List


@dataclass
class ProjectInput:
    """

    Attributes:
        name (str): The name that you would like to assign to the new Project. The Project name must be unique.
        groups (`list` of `str`): The group IDs of Groups (of users) that you would like to assign to this Project.
                     The ID of a Group can be found using the GET /auth/groups API.
                      A group must already exist in your account before a Project can be assigned to it.
                       Only users assigned to the designated Groups will have access to this Project.
        repo_url (str): The Git repo URL.
        main_branch (str): The Git branch of the source code that is designated as “primary” for this Project.
        origin (str): The manner by which the Project was created.
        tags (dict): The tags you want assigned to the Project.
                    Tags need to be formatted in key-value pairs.
                    example:
                    "tags": {"Tag01": "", "Severity": "high"}
        criticality (int):
            minimum: 1
            maximum: 5
            default: 3
            example: 3
            Criticality level of the project
    """
    name: str = None
    groups: List[str] = None
    repo_url: str = None
    main_branch: str = None
    origin: str = None
    tags: dict = None
    criticality: int = None

    def to_dict(self):
        data = {}
        if self.name:
            data.update({"name": self.name})
        if self.groups:
            data.update({"groups": self.groups})
        if self.repo_url:
            data.update({"repoUrl": self.repo_url})
        if self.main_branch:
            data.update({"mainBranch": self.main_branch})
        if self.origin:
            data.update({"origin": self.origin})
        if self.tags:
            data.update({"tags": self.tags})
        if self.criticality:
            data.update({"criticality": self.criticality})
        return data
