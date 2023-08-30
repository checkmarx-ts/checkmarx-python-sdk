# encoding: utf-8
from .httpRequests import get_request, post_request
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .utilities import type_check
from .dto import (
    scmOrg,
    ReposCollection,
    OrgRepo
)

def __construct_repo(repo):
    return OrgRepo(
        id=repo.get("id"),
        name=repo.get("name"),
        url=repo.get("url"),
        defaultBranch=repo.get("defaultBranch"),
        fullName=repo.get("fullName"),
        isRepoAdmin=repo.get("isRepoAdmin"),
        privatePackage=repo.get("privatePackage"),
        sshRepoUrl=repo.get("sshRepoUrl")
    )

def get_scm_orgs():
    """

    Returns:
        json
        example: {
          "id": "",
          "name":  "",
          "isUser": ""
        }
    """

    relative_url = "/api/repos-manager/scms/1/user/orgs?authCode=d2e5714b965c732d57eb"
    response = get_request(relative_url=relative_url)
    return response.json()

def get_org_repos(org):
    """

    Returns: ReposCollection

    """

    type_check(org, str)
    relative_url = "/api/repos-manager/scms/1/orgs/{org}/repos?authCode=d2e5714b965c732d57eb&isUser=false&page=1".format(org=org)
    response = get_request(relative_url=relative_url)
    item = response.json()
    return ReposCollection(
        total_count=item.get("totalCount"),
        repos=[
            __construct_repo(repo) for repo in item.get("repoWebDtoList") or []
        ]
    )

def import_repo(RepoInput, org):
    """

    Args:
        RepoInput: RepoScmImportInput
        org: Name of org

    Returns:
        json:
        example: {
                    "orgConfigResult": {
                        "orgIdentity": "org",
                        "status": "SUCCESS"
                    },
                    "repoConfigResultList": [
                        {
                            "repoId": 12345,
                            "projectId": "1234-1234-1234-124",
                            "repoIdentity": "repoName",
                            "repoUrl": "url",
                            "status": "SUCCESS",
                            "name": "name"
                        }
                    ]
                }

    """
    relative_url = "/api/repos-manager/scms/1/orgs/{org}/repos?authCode=d2e5714b965c732d57eb&isUser=false&isOrgWebhookEnabled=true&createAstProject=true&scanAstProject=true".format(org=org)
    data = RepoInput.get_post_data()
    response = post_request(relative_url=relative_url, data=data)
    item = response.json()
    return item