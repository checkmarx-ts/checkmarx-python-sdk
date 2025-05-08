import json
from .httpRequests import get_request, post_request
from typing import List

origin_dict = {
    "GITHUB": 1,
    "GITLAB": 2,
    "AZURE": 3,
    "BITBUCKET": 4,
}


def get_repos(origin: str, organization: str, auth_code: str, is_user: bool = False, page: int = 1):
    assert origin in origin_dict.keys()
    relative_url = f"/api/repos-manager/scms/{origin_dict.get(origin)}/orgs/{organization}/repos"
    params = {
        "authCode": auth_code,
        "isUser": str(is_user).lower(),
        "page": page,
    }
    return get_request(relative_url=relative_url, params=params)


def get_repo_branches(origin: str, organization: str, repo: str, auth_code: str, page: int = 1):
    assert origin in origin_dict.keys()
    relative_url = f"/api/repos-manager/scms/{origin_dict.get(origin)}/orgs/{organization}/repos/{repo}/branches"
    params = {
        "authCode": auth_code,
        "page": page,
    }
    return get_request(relative_url=relative_url, params=params)


def github_import(github_org: str, auth_code: str, repos_from_request: List[dict],
                  is_user: bool = False, is_org_webhook_enabled: bool = True, create_ast_project: bool = True,
                  scan_ast_project: bool = False):
    """

    Args:
        github_org (str):
        auth_code (str):
        repos_from_request (List[dict]): the dict has url and default_branch keys
        is_user (bool):
        is_org_webhook_enabled (bool):
        create_ast_project (bool):
        scan_ast_project (bool):

    Returns:

    """
    relative_url = f"/api/repos-manager/scms/1/orgs/{github_org}/asyncImport"
    return repo_import(relative_url=relative_url, auth_code=auth_code, repos_from_request=repos_from_request,
                       is_user=is_user, is_org_webhook_enabled=is_org_webhook_enabled,
                       create_ast_project=create_ast_project,
                       scan_ast_project=scan_ast_project)


def construct_repo_request(
        http_repo_url, ssh_repo_url, id=None, branches: List[dict] = None, is_repo_admin=True, origin="GITHUB",
        kics_scanner_enabled=True, sast_incremental_scan=True, sast_scanner_enabled=True,
        api_sec_scanner_enabled=True, sca_scanner_enabled=True, webhook_enabled=True, pre_decoration_enabled=True,
        sca_auto_pr_enabled=True, container_scanner_enabled=True, ossf_score_card_scanner_enabled=True,
        secrets_detection_scanner_enabled=True, name=None, project_id=None):
    """

    Args:
        http_repo_url:
        ssh_repo_url:
        id:
        branches: example: [
                {
                    "name": "master",
                    "isDefaultBranch": True
                }
            ]
        is_repo_admin:
        origin:
        kics_scanner_enabled:
        sast_incremental_scan:
        sast_scanner_enabled:
        api_sec_scanner_enabled:
        sca_scanner_enabled:
        webhook_enabled:
        pre_decoration_enabled:
        sca_auto_pr_enabled:
        container_scanner_enabled:
        ossf_score_card_scanner_enabled:
        secrets_detection_scanner_enabled:
        name:
        project_id:

    Returns:

    """
    http_repo_url = http_repo_url.replace(".git", "")
    org_repo_name = "/".join(http_repo_url.split("/")[3:])
    if origin in ["AZURE", "BITBUCKET"]:
        org_repo_name = "/".join(org_repo_name.split("/")[0:2])
    repo_name = org_repo_name.split("/")[1]
    data = {
        "id": repo_name,
        "isRepoAdmin": is_repo_admin,
        "name": org_repo_name,
        "origin": origin,
        "url": http_repo_url,
        "branches": branches,
        "kicsScannerEnabled": kics_scanner_enabled,
        "sastIncrementalScan": sast_incremental_scan,
        "sastScannerEnabled": sast_scanner_enabled,
        "apiSecScannerEnabled": api_sec_scanner_enabled,
        "scaScannerEnabled": sca_scanner_enabled,
        "webhookEnabled": webhook_enabled,
        "prDecorationEnabled": pre_decoration_enabled,
        "scaAutoPrEnabled": sca_auto_pr_enabled,
        "sshRepoUrl": ssh_repo_url,
        "sshState": "SKIPPED",
        "containerScannerEnabled": container_scanner_enabled,
        "ossfSecoreCardScannerEnabled": ossf_score_card_scanner_enabled,
        "secretsDerectionScannerEnabled": secrets_detection_scanner_enabled
    }
    if origin in ['GITLAB', "BITBUCKET"]:
        data.update({"id": id})
    if origin in ["AZURE"]:
        data.update({
            "id": id,
            "projectId": project_id,
        })
    return data


def construct_github_repo_request(
        http_repo_url, ssh_repo_url, branches, is_repo_admin=True, origin="GITHUB",
        kics_scanner_enabled=True, sast_incremental_scan=True, sast_scanner_enabled=True,
        api_sec_scanner_enabled=True, sca_scanner_enabled=True, webhook_enabled=True, pre_decoration_enabled=True,
        sca_auto_pr_enabled=True, container_scanner_enabled=True, ossf_score_card_scanner_enabled=True,
        secrets_detection_scanner_enabled=True):
    return construct_repo_request(
        http_repo_url=http_repo_url, ssh_repo_url=ssh_repo_url, branches=branches,
        is_repo_admin=is_repo_admin, origin=origin,
        kics_scanner_enabled=kics_scanner_enabled, sast_incremental_scan=sast_incremental_scan,
        sast_scanner_enabled=sast_scanner_enabled, api_sec_scanner_enabled=api_sec_scanner_enabled,
        sca_scanner_enabled=sca_scanner_enabled, webhook_enabled=webhook_enabled,
        pre_decoration_enabled=pre_decoration_enabled, sca_auto_pr_enabled=sca_auto_pr_enabled,
        container_scanner_enabled=container_scanner_enabled,
        ossf_score_card_scanner_enabled=ossf_score_card_scanner_enabled,
        secrets_detection_scanner_enabled=secrets_detection_scanner_enabled)


def repo_import(relative_url: str, auth_code: str, repos_from_request: List[dict],
                is_user: bool = False, is_org_webhook_enabled: bool = False, create_ast_project: bool = True,
                scan_ast_project: bool = False):
    """

    Args:
        relative_url (str):
        auth_code (str):
        repos_from_request (List[dict]): the dict has url and default_branch keys
        is_user (bool):
        is_org_webhook_enabled (bool):
        create_ast_project (bool):
        scan_ast_project (bool):

    Returns:

    """
    params = {
        "authCode": auth_code,
        "isUser": str(is_user).lower(),
        "isOrgWebhookEnabled": str(is_org_webhook_enabled).lower(),
        "createAstProject": str(create_ast_project).lower(),
        "scanAstProject": str(scan_ast_project).lower()
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "strict-transport-security": "max-age=31536000; includeSubDomains",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/134.0.0.0 Safari/537.36",
        "webapp": "true",
        'Accept-Encoding': 'identity',
    }

    data = {
        "reposFromRequest": repos_from_request,
        "orgSshKey": "",
        "orgSshState": "SKIPPED"
    }
    response = post_request(relative_url=relative_url, params=params, headers=headers, json=data)
    return response


def gitlab_import(gitlab_org: str, auth_code: str, repos_from_request: List[dict],
                  is_user: bool = False, is_org_webhook_enabled: bool = False, create_ast_project: bool = True,
                  scan_ast_project: bool = False):
    relative_url = f"/api/repos-manager/scms/2/orgs/{gitlab_org}/repos"
    return repo_import(relative_url=relative_url, auth_code=auth_code, repos_from_request=repos_from_request,
                       is_user=is_user, is_org_webhook_enabled=is_org_webhook_enabled,
                       create_ast_project=create_ast_project,
                       scan_ast_project=scan_ast_project)


def azure_import(azure_org: str, auth_code: str, repos_from_request: List[dict],
                 is_user: bool = False, is_org_webhook_enabled: bool = False, create_ast_project: bool = True,
                 scan_ast_project: bool = False):
    relative_url = f"/api/repos-manager/scms/3/orgs/{azure_org}/repos"
    return repo_import(relative_url=relative_url, auth_code=auth_code, repos_from_request=repos_from_request,
                       is_user=is_user, is_org_webhook_enabled=is_org_webhook_enabled,
                       create_ast_project=create_ast_project,
                       scan_ast_project=scan_ast_project)


def construct_bitbucket_repo_request(
        http_repo_url, ssh_repo_url, branches, is_repo_admin=True, origin="BITBUCKET",
        kics_scanner_enabled=True, sast_incremental_scan=True, sast_scanner_enabled=True,
        api_sec_scanner_enabled=True, sca_scanner_enabled=True, webhook_enabled=True, pre_decoration_enabled=True,
        sca_auto_pr_enabled=True, container_scanner_enabled=True, ossf_score_card_scanner_enabled=True,
        secrets_detection_scanner_enabled=True):
    """

    Args:
        http_repo_url:
        ssh_repo_url:
        branches: example: [{
                "name": "master",
                "isDefaultBranch": False,
                "bitBucketBranchCommitHash": "f96f204bc2546f3a7568da24f6215cf6d4387112"
            }]
        is_repo_admin:
        origin:
        kics_scanner_enabled:
        sast_incremental_scan:
        sast_scanner_enabled:
        api_sec_scanner_enabled:
        sca_scanner_enabled:
        webhook_enabled:
        pre_decoration_enabled:
        sca_auto_pr_enabled:
        container_scanner_enabled:
        ossf_score_card_scanner_enabled:
        secrets_detection_scanner_enabled:

    Returns:

    """
    return construct_repo_request(
        http_repo_url=http_repo_url, ssh_repo_url=ssh_repo_url, branches=branches,
        is_repo_admin=is_repo_admin, origin=origin, kics_scanner_enabled=kics_scanner_enabled,
        sast_incremental_scan=sast_incremental_scan, sast_scanner_enabled=sast_scanner_enabled,
        api_sec_scanner_enabled=api_sec_scanner_enabled, sca_scanner_enabled=sca_scanner_enabled,
        webhook_enabled=webhook_enabled, pre_decoration_enabled=pre_decoration_enabled,
        sca_auto_pr_enabled=sca_auto_pr_enabled, container_scanner_enabled=container_scanner_enabled,
        ossf_score_card_scanner_enabled=ossf_score_card_scanner_enabled,
        secrets_detection_scanner_enabled=secrets_detection_scanner_enabled)


def bitbucket_import(bitbucket_org: str, auth_code: str, repos_from_request: List[dict],
                     is_user: bool = False, is_org_webhook_enabled: bool = False, create_ast_project: bool = True,
                     scan_ast_project: bool = False):
    relative_url = f"api/repos-manager/scms/4/orgs/{bitbucket_org}/repos"
    return repo_import(relative_url=relative_url, auth_code=auth_code, repos_from_request=repos_from_request,
                       is_user=is_user, is_org_webhook_enabled=is_org_webhook_enabled,
                       create_ast_project=create_ast_project,
                       scan_ast_project=scan_ast_project)


def get_job_status():
    relative_url = "/api/ssegateway/job-status"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/134.0.0.0 Safari/537.36",
        'Accept-Encoding': 'identity',
    }
    response = get_request(relative_url, headers=headers)
    data_list = [json.loads(item.replace("data:", "")) for item in response.text.split("\n") if item != ""]
    job_percentage = data_list[-1].get("percentage")
    return job_percentage
