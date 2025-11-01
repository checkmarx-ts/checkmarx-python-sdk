from dataclasses import dataclass
from typing import List


@dataclass
class RichProject:
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
    "applicationIds": []
    }
    Attributes:
        id (str): A unique identifier for a project
        name (str): The project name
        application_ids (list of str): The applications this project is associated to
        groups (list of str): The groups authorized for this project
        repo_url (str): The reprosentive repository URL
        main_branch (str): The Git main branch
        origin (str): The origin of project
        created_at (str):
        updated_at (str):
        tags (dict):
        criticality (int):
            minimum: 1
            maximum: 5
            default: 3
            example: 3
            Criticality level of the project
        repo_id (int): The id of the repository
        scm_repo_id (str): The SCM repository id
    """

    id: str
    name: str = None
    application_ids: List[str] = None
    groups: List[str] = None
    repo_url: str = None
    main_branch: str = None
    origin: str = None
    created_at: str = None
    updated_at: str = None
    tags: dict = None
    criticality: int = 3
    repo_id: int = None
    scm_repo_id: str = None

def construct_rich_project(item):
    return RichProject(
        id=item.get("id"),
        name=item.get("name"),
        application_ids=item.get("applicationIds"),
        groups=item.get("groups"),
        repo_url=item.get("repoUrl"),
        main_branch=item.get("mainBranch"),
        origin=item.get("origin"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt"),
        tags=item.get("tags"),
        criticality=item.get("criticality"),
        repo_id=item.get("repoId"),
        scm_repo_id=item.get("scmRepoId")
    )
