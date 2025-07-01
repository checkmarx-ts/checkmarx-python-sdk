# encoding: utf-8
class RichProject(object):
    """
    {
    "id": "62b18663-16c7-4da9-ab9f-c685120b31e3",
    "name": "happy-cook/JavaVulnerableLab",
    "tenantId": "71fe66b9-b3ea-4fc7-8594-541d0a07a697",
    "createdAt": "2025-07-01T01:23:21.015568Z",
    "updatedAt": "2025-07-01T01:23:21.015568Z",
    "groups": [],
    "tags": {},
    "repoUrl": "",
    "mainBranch": "",
    "origin": "GitHub",
    "scmRepoId": "JavaVulnerableLab",
    "repoId": 174896,
    "criticality": 0,
    "privatePackage": false,
    "imported_proj_name": "happy-cook/JavaVulnerableLab",
    "applicationIds": []
    }
    """
    def __init__(self, project_id, name=None, application_ids=None, groups=None,
                 repo_url=None, main_branch=None, origin=None,
                 created_at=None, updated_at=None, tags=None, criticality=3,
                 tenant_id=None, scm_repo_id=None, repo_id=None, private_package=None,
                 imported_proj_name=None):
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
            tenant_id (str):
            scm_repo_id (str):
            repo_id (int):
            private_package (bool):
            imported_proj_name (str):
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
        self.tenantId = tenant_id
        self.scmRepoId = scm_repo_id
        self.repoId = repo_id
        self.privatePackage = private_package
        self.imported_proj_name = imported_proj_name

    def __str__(self):
        return """RichProject(id={}, name={}, applicationIds={}, groups={}, repoUrl={}, mainBranch={}, 
        origin={}, createdAt={}, updatedAt={}, tags={}, criticality={}, tenantId={}, scmRepoId={}, repoId={},
        privatePackage={}, imported_proj_name={})""".format(
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
            self.tenantId,
            self.scmRepoId,
            self.repoId,
            self.privatePackage,
            self.imported_proj_name,
        )
