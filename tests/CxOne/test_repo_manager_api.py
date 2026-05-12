import os
from dotenv import load_dotenv
from CheckmarxPythonSDK.CxOne import (
    RepoManagerAPI,
    get_repos,
    get_repo_branches,
    construct_repo_request,
    repo_import,
    get_job_status,
    batch_import_repo,
    get_repo_by_id,
    update_repo_by_id,
)


load_dotenv("E:\github.com\checkmarx-python-sdk\happy.env") 
repo_manager = RepoManagerAPI()

def test_get_all_scm_types_v2():
    all_scm_types = repo_manager.get_all_scm_types_v2()
    for scm in all_scm_types:
        print(scm)
    assert len(all_scm_types) > 1


def test_get_verify_status_for_user():
    result = repo_manager.get_verify_status_for_user(
        origin="GITHUBAPP",
        auth_code=os.getenv("GITHUBAPP_AUTH_CODE")
    )
    assert result is True


def test_get_github_app_info():
    result = repo_manager.get_github_app_info(
        auth_code=os.getenv("GITHUBAPP_AUTH_CODE")
    )
    print(result)
    assert result is not None

def test_create_token_for_github_app():
    result = repo_manager.create_token_for_github_app(
        auth_code=os.getenv("GITHUBAPP_AUTH_CODE")
    )
    assert result is True

def test_get_all_repo_orgs_for_a_scm_type():
    repo_orgs = repo_manager.get_all_repo_orgs_for_a_scm_type(
        origin="GITHUBAPP",
        auth_code=os.getenv("GITHUBAPP_AUTH_CODE"),
        page=1,
        page_size=50,
    )
    for repo_org in repo_orgs.orgs:
        print(type(repo_org))
        print(repo_org)
    assert len(repo_orgs.orgs) > 0


def test_create_installation_of_scm_on_org():
    installation = repo_manager.create_installation_of_scm_on_org(
        origin="GITHUBAPP",
        auth_code=os.getenv("GITHUBAPP_AUTH_CODE"),
        org_name="happy-cook",
    )
    print(installation)
    assert installation is not None


def test_get_all_repos_of_an_org_for_a_scm():
    installation = repo_manager.create_installation_of_scm_on_org(
        origin="GITHUBAPP",
        auth_code=os.getenv("GITHUBAPP_AUTH_CODE"),
        org_name="happy-cook",
    )
    all_repos = repo_manager.get_all_repos_of_an_org_for_a_scm(
        origin="GITHUBAPP",
        org_name="happy-cook",
        token_id=installation.tokenId,
        is_user=False,
    )
    for repo in all_repos.repos:
        print(type(repo))
        print(repo)
    assert len(all_repos.repos) > 0


def test_github_app_import():
    github_org = "happy-cook"
    auth_code = os.getenv("GITHUBAPP_AUTH_CODE")
    origin = "GITHUBAPP"
    installation = repo_manager.create_installation_of_scm_on_org(
        origin="GITHUBAPP",
        auth_code=os.getenv("GITHUBAPP_AUTH_CODE"),
        org_name="happy-cook",
    )
    all_repos = repo_manager.get_all_repos_of_an_org_for_a_scm(
        origin="GITHUBAPP",
        org_name="happy-cook",
        token_id=installation.tokenId,
        is_user=False,
    )
    repo_requests = [repo_manager.construct_repo_request(
        http_repo_url=repo.url,
        repo_id=repo.id,
        branches=[{
            "pattern": repo.defaultBranch,
            "isDefaultBranch": True
        }],
        origin="GITHUBAPP",
        webhook_enabled=True,
    ) for repo in all_repos.repos if repo.name != "WebGoat"]
    for repo_request in repo_requests:
        print(repo_request)
    response = repo_manager.repo_import(
        origin=origin, 
        organization=github_org, 
        auth_code=None, 
        token_id=installation.tokenId,
        repos_from_request=repo_requests,
        is_user=False, 
        is_org_webhook_enabled=False, 
        create_ast_project=True,
        scan_ast_project=False
    )
    assert response.status_code == 201

def test_github_import():
    github_org = "happy-cook"
    auth_code = os.getenv("CXONE_GITHUB_AUTH_CODE")
    origin = "GITHUB"
    repos = get_repos(origin=origin, organization=github_org, auth_code=auth_code).json().get("repoWebDtoList")
    repo_request = [construct_repo_request(
        http_repo_url=repo.get("url"),
        ssh_repo_url=repo.get("sshRepoUrl"),
        repo_id=repo.get("id"),
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
        repo_id=repo.get("id"),
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
        repo_id=repo.get("id"),
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
            repo_id=repo.get("id"),
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
