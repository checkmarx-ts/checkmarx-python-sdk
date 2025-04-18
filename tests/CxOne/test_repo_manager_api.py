import os
from CheckmarxPythonSDK.CxOne import (
    get_repos,
    get_repo_branches,
    construct_repo_request,
    construct_github_repo_request,
    repo_import,
    github_import,
    gitlab_import,
    azure_import,
    construct_bitbucket_repo_request,
    bitbucket_import,
    get_job_status,
)


def test_github_import():
    github_org = "happy-cook"
    auth_code = os.getenv("CXONE_GITHUB_AUTH_CODE")
    repos = get_repos(origin="GITHUB", organization=github_org, auth_code=auth_code).json().get("repoWebDtoList")
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
    response = github_import(github_org=github_org, auth_code=auth_code, repos_from_request=repo_request,
                             is_user=True, is_org_webhook_enabled=True, create_ast_project=True,
                             scan_ast_project=False)
    assert response.status_code == 201


def test_gitlab_import():
    gitlab_org = "happy-gitlab"
    auth_code = os.getenv("CXONE_GITLAB_AUTH_CODE")
    repos = get_repos(origin="GITLAB", organization=gitlab_org, auth_code=auth_code).json().get("repoWebDtoList")
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
    response = gitlab_import(gitlab_org=gitlab_org, auth_code=auth_code, repos_from_request=repo_request)
    assert response.status_code == 200


def test_azure_import():
    azure_org = "HappyYang0077"
    auth_code = os.getenv("CXONE_AZURE_AUTH_CODE")
    repos = get_repos(origin="AZURE", organization=azure_org, auth_code=auth_code).json().get("repoWebDtoList")
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
    response = azure_import(azure_org=azure_org, auth_code=auth_code, repos_from_request=repo_request)
    assert response.status_code == 200


def test_bitbucket_import():
    bitbucket_org = "happyy19"
    auth_code = os.getenv("CXONE_BITBUCKET_AUTH_CODE")
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
    response = bitbucket_import(bitbucket_org=bitbucket_org, auth_code=auth_code, repos_from_request=repo_requests)
    assert response.status_code == 200
