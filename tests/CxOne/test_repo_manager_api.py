import os
from CheckmarxPythonSDK.CxOne import (
    get_repos,
    get_repo_branches,
    construct_repo_request,
    repo_import,
    get_job_status,
    batch_import_repo,
    get_repo_by_id,
    update_repo_by_id,
)


def test_github_import():
    github_org = "happy-cook"
    auth_code = os.getenv("CXONE_GITHUB_AUTH_CODE")
    origin = "GITHUB"
    repos = get_repos(origin=origin, organization=github_org, auth_code=auth_code).json().get("repoWebDtoList")
    repo_request = [construct_repo_request(
        http_repo_url=repo.get("url"),
        ssh_repo_url=repo.get("sshRepoUrl"),
        id=repo.get("id"),
        branches=[{
            "name": repo.get("defaultBranch"),
            "isDefaultBranch": True
        }],
        origin="GITHUB",
        webhook_enabled=True,
    ) for repo in repos]
    response = repo_import(origin=origin, organization=github_org, auth_code=auth_code, repos_from_request=repo_request,
                           is_user=True, is_org_webhook_enabled=True, create_ast_project=True,
                           scan_ast_project=False)
    assert response.status_code == 201


def test_gitlab_import():
    gitlab_org = "happy-gitlab"
    auth_code = os.getenv("CXONE_GITLAB_AUTH_CODE")
    origin = "GITLAB"
    repos = get_repos(origin=origin, organization=gitlab_org, auth_code=auth_code).json().get("repoWebDtoList")
    repo_request = [construct_repo_request(
        http_repo_url=repo.get("url"),
        ssh_repo_url=repo.get("sshRepoUrl"),
        id=repo.get("id"),
        branches=[{
            "name": repo.get("defaultBranch"),
            "isDefaultBranch": True
        }],
        origin="GITLAB",
    ) for repo in repos]
    response = repo_import(origin=origin, organization=gitlab_org, auth_code=auth_code, repos_from_request=repo_request)
    assert response.status_code == 200


def test_azure_import():
    azure_org = "HappyYang0077"
    auth_code = os.getenv("CXONE_AZURE_AUTH_CODE")
    origin = "AZURE"
    repos = get_repos(origin=origin, organization=azure_org, auth_code=auth_code).json().get("repoWebDtoList")
    repo_request = [construct_repo_request(
        http_repo_url=repo.get("url"),
        ssh_repo_url=repo.get("sshRepoUrl"),
        id=repo.get("id"),
        branches=[{
            "name": repo.get("defaultBranch"),
            "isDefaultBranch": True
        }],
        origin="AZURE",
        project_id=repo.get("projectId"),
        webhook_enabled=True,
    ) for repo in repos]
    response = repo_import(origin=origin, organization=azure_org, auth_code=auth_code, repos_from_request=repo_request)
    assert response.status_code == 200


def test_bitbucket_import():
    bitbucket_org = "happyy19"
    auth_code = os.getenv("CXONE_BITBUCKET_AUTH_CODE")
    origin = "BITBUCKET"
    repos = get_repos(origin="BITBUCKET", organization=bitbucket_org, auth_code=auth_code).json().get("repoWebDtoList")
    repo_requests = []
    for repo in repos:
        if repo.get("id") != "javavulnerablelab":
            continue
        branches = get_repo_branches(
            origin="BITBUCKET",
            organization=bitbucket_org,
            repo="javavulnerablelab",
            auth_code=auth_code,
            page=1
        ).json().get('branchWebDtoList')
        repo_request = construct_repo_request(
            http_repo_url=repo.get("url"),
            ssh_repo_url=repo.get("sshRepoUrl"),
            id=repo.get("id"),
            branches=list(filter(lambda r: r.get("name") == "master", branches)),
            origin="BITBUCKET",
            webhook_enabled=True,
        )
        repo_requests.append(repo_request)
    response = repo_import(origin=origin, organization=bitbucket_org, auth_code=auth_code,
                           repos_from_request=repo_requests)
    assert response.status_code == 200


def test_get_repo_by_id():
    result = get_repo_by_id(repo_id=174896)
    assert result is not None


def test_update_repo_by_id():
    result = update_repo_by_id(repo_id=174896, project_id="62b18663-16c7-4da9-ab9f-c685120b31e3",
                               pay_load={
                                   "branches": [{"name": "master", "isDefaultBranch": True}],
                                   "kicsScannerEnabled": True,
                                   "sastIncrementalScan": True,
                                   "sastScannerEnabled": True,
                                   "scaScannerEnabled": True,
                                   "apiSecScannerEnabled": True,
                                   "url": "https://github.com/happy-cook/JavaVulnerableLab",
                                   "webhookEnabled": True,
                                   "prDecorationEnabled": False,
                                   "secretsDerectionScannerEnabled": True,
                                   "ossfSecoreCardScannerEnabled": True,
                                   "scaAutoPrEnabled": False,
                                   "webhookId": "555312209",
                                   "sshRepoUrl": "git@github.com:happy-cook/JavaVulnerableLab.git",
                                   "sshState": "SKIPPED",
                                   "isRepoAdmin": True,
                                   "containerScannerEnabled": True
                               }
                               )
    assert result is not None
