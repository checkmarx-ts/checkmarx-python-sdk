# encoding: utf-8
import json
from ..utilities import type_check, list_member_type_check


class ProjectInput(object):
    def __init__(self, name=None, groups=None, repo_url=None, main_branch=None, origin=None, tags=None, criticality=3):
        """

        Args:
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
        type_check(name, str)
        type_check(groups, (list, tuple))
        list_member_type_check(groups, str)
        type_check(repo_url, str)
        type_check(main_branch, str)
        type_check(origin, str)
        type_check(tags, dict)
        type_check(criticality, int)

        self.name = name
        self.groups = groups
        self.repoUrl = repo_url
        self.mainBranch = main_branch
        self.origin = origin
        self.tags = tags
        self.criticality = criticality

    def __str__(self):
        return """ProjectInput(name={}, groups={}, repoUrl={}, mainBranch={}, origin={}, tags={}, 
        criticality={})""".format(
            self.name,
            self.groups,
            self.repoUrl,
            self.mainBranch,
            self.origin,
            self.tags,
            self.criticality,
        )

    def get_post_data(self):
        data = {}
        if self.name:
            data.update({"name": self.name})
        if self.groups:
            data.update({"groups": self.groups})
        if self.repoUrl:
            data.update({"repoUrl": self.repoUrl})
        if self.mainBranch:
            data.update({"mainBranch": self.mainBranch})
        if self.origin:
            data.update({"origin": self.origin})
        if self.tags:
            data.update({"tags": self.tags})

        return json.dumps(data)
