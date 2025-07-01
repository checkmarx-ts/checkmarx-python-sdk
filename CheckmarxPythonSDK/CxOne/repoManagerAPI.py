import math
import json
import time
import logging
from .httpRequests import get_request, post_request, put_request
from typing import List
from requests.exceptions import ChunkedEncodingError
from .projectsAPI import get_all_projects

logger = logging.getLogger("CheckmarxPythonSDK")

origin_dict = {
    "GITHUB": 1,
    "GITLAB": 2,
    "AZURE": 3,
    "BITBUCKET": 4,
}


def check_origin(origin: str) -> str:
    origin = origin.upper()
    if origin not in origin_dict.keys():
        raise ValueError(f"origin {origin} not support! Currently only support GITHUB, GITLAB, AZURE, BITBUCKET")
    return origin


def get_repos(origin: str, organization: str, auth_code: str, is_user: bool = False, page: int = 1):
    origin = check_origin(origin)
    relative_url = f"/api/repos-manager/scms/{origin_dict.get(origin)}/orgs/{organization}/repos"
    params = {
        "authCode": auth_code,
        "isUser": str(is_user).lower(),
        "page": page,
    }
    return get_request(relative_url=relative_url, params=params)


def get_all_repos(origin: str, organization: str, auth_code: str, is_user: bool = False):
    origin = check_origin(origin)
    result = []
    page = 1
    while True:
        repos = get_repos(
            origin=origin, organization=organization, auth_code=auth_code, is_user=is_user, page=page
        ).json().get("repoWebDtoList")
        page += 1
        if not repos:
            break
        result.extend(repos)
    return result


def get_repo_branches(origin: str, organization: str, repo_name: str, auth_code: str, page: int = 1):
    origin = check_origin(origin)
    relative_url = f"/api/repos-manager/scms/{origin_dict.get(origin)}/orgs/{organization}/repos/{repo_name}/branches"
    params = {
        "authCode": auth_code,
        "page": page,
    }
    return get_request(relative_url=relative_url, params=params)


def get_all_repo_branches(origin: str, organization: str, repo_name: str, auth_code: str):
    origin = check_origin(origin)
    result = []
    page = 1
    while True:
        repos = get_repo_branches(
            origin=origin, organization=organization, repo_name=repo_name, auth_code=auth_code, page=page
        ).json().get("branchWebDtoList")
        page += 1
        if not repos:
            break
        result.extend(repos)
    return result


def construct_repo_request(
        http_repo_url, ssh_repo_url, id=None, branches: List[dict] = None, is_repo_admin=True, origin="GITHUB",
        kics_scanner_enabled=True, sast_incremental_scan=True, sast_scanner_enabled=True,
        api_sec_scanner_enabled=True, sca_scanner_enabled=True, webhook_enabled=True, pr_decoration_enabled=True,
        sca_auto_pr_enabled=False, container_scanner_enabled=True, ossf_score_card_scanner_enabled=True,
        secrets_detection_scanner_enabled=True, project_id=None):
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
        pr_decoration_enabled:
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
        "prDecorationEnabled": pr_decoration_enabled,
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


def repo_import(origin: str, organization: str, auth_code: str, repos_from_request: List[dict],
                is_user: bool = False, is_org_webhook_enabled: bool = False, create_ast_project: bool = True,
                scan_ast_project: bool = False):
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
    relative_url = f"/api/repos-manager/scms/{origin_dict.get(origin)}/orgs/{organization}/"
    if origin == "GITHUB":
        relative_url += "asyncImport"
    else:
        relative_url += "repos"
    response = post_request(relative_url=relative_url, params=params, headers=headers, json=data)
    return response


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


def batch_import_repo(repos: List[dict], origin: str, organization: str, auth_code: str, chunk_size: int = 200,
                      is_user: bool = False, is_org_webhook_enabled: bool = False,
                      create_ast_project: bool = True, scan_ast_project: bool = False,
                      kics_scanner_enabled=True, sast_incremental_scan=True, sast_scanner_enabled=True,
                      api_sec_scanner_enabled=True, sca_scanner_enabled=True, webhook_enabled=True,
                      pr_decoration_enabled=True,
                      sca_auto_pr_enabled=False, container_scanner_enabled=True, ossf_score_card_scanner_enabled=True,
                      secrets_detection_scanner_enabled=True
                      ):
    origin = check_origin(origin)
    project_list = get_all_projects()
    project_name_list = [project.name for project in project_list]
    repo_requests = []
    for repo in repos:
        repo_full_name = repo.get("fullName")
        if repo_full_name in project_name_list:
            logger.info(f"repo {repo_full_name} already exist in cx one, skip!")
            continue
        repo_requests.append(
            construct_repo_request(
                http_repo_url=repo.get("url"),
                ssh_repo_url=repo.get("sshRepoUrl"),
                id=repo.get("id"),
                branches=[{
                    "name": repo.get("defaultBranch"),
                    "isDefaultBranch": True
                }],
                origin=origin,
                kics_scanner_enabled=kics_scanner_enabled,
                sast_incremental_scan=sast_incremental_scan,
                sast_scanner_enabled=sast_scanner_enabled,
                api_sec_scanner_enabled=api_sec_scanner_enabled,
                sca_scanner_enabled=sca_scanner_enabled,
                webhook_enabled=webhook_enabled,
                pr_decoration_enabled=pr_decoration_enabled,
                sca_auto_pr_enabled=sca_auto_pr_enabled,
                container_scanner_enabled=container_scanner_enabled,
                ossf_score_card_scanner_enabled=ossf_score_card_scanner_enabled,
                secrets_detection_scanner_enabled=secrets_detection_scanner_enabled,
            )
        )
    round_of_requests = math.ceil(len(repos) / chunk_size)
    logger.info(f"there are total {len(repos)} repos in org: {organization}, "
                f"total {len(repo_requests)} repo requests created, "
                f"will be {round_of_requests} round_of_requests ")
    round_i = 0
    while round_i < round_of_requests:
        repo_request_chunks = repo_requests[round_i * chunk_size: (round_i + 1) * chunk_size + 1]
        logger.info(f"round {round_i + 1}, number of repos to create: {len(repo_request_chunks)} ")
        round_i += 1
        repo_import(
            origin=origin, organization=organization, auth_code=auth_code, repos_from_request=repo_request_chunks,
            is_user=is_user, is_org_webhook_enabled=is_org_webhook_enabled, create_ast_project=create_ast_project,
            scan_ast_project=scan_ast_project
        )
        percentage = 0
        while percentage < 100:
            try:
                percentage = get_job_status()
                logger.info(f"import percent: {percentage}")
                time.sleep(10)
            except ChunkedEncodingError as e:
                logger.info(f"ChunkedEncodingError: {e}")
                continue
        time.sleep(10)


def get_repo_by_id(repo_id: int):
    """

    Args:
        repo_id:

    Returns:
        example:
        {
    "id": "174896",
    "url": "https://github.com/happy-cook/JavaVulnerableLab",
    "webhookId": "555312209",
    "webhookEnabled": true,
    "prDecorationEnabled": false,
    "isRepoAdmin": true,
    "sastIncrementalScan": true,
    "sastScannerEnabled": true,
    "scaScannerEnabled": true,
    "kicsScannerEnabled": true,
    "apiSecScannerEnabled": true,
    "containerScannerEnabled": true,
    "ossfSecoreCardScannerEnabled": true,
    "secretsDerectionScannerEnabled": true,
    "privatePackage": false,
    "branches": [
        {
            "name": "master",
            "isDefaultBranch": true
        }
    ],
    "sshRepoUrl": "git@github.com:happy-cook/JavaVulnerableLab.git",
    "scmId": 1,
    "scm": {
        "typeName": "github"
    },
    "scaAutoPrEnabled": false,
    "kicsAutoPrEnabled": false,
    "sastAutoPrEnabled": false
    }

    """

    relative_url = f"/api/repos-manager/repo/{repo_id}"
    response = get_request(relative_url)
    return response.json()


def update_repo_by_id(repo_id: int, project_id: str, pay_load: dict):
    """

    Args:
        repo_id (int):
        project_id (str):
        pay_load (dict):
            {
            "branches":[{"name":"master","isDefaultBranch":true}],
            "kicsScannerEnabled":true,
            "sastIncrementalScan":true,
            "sastScannerEnabled":true,
            "scaScannerEnabled":true,
            "apiSecScannerEnabled":true,
            "url":"https://github.com/happy-cook/JavaVulnerableLab",
            "webhookEnabled":true,
            "prDecorationEnabled":false,
            "secretsDerectionScannerEnabled":true,
            "ossfSecoreCardScannerEnabled":true,
            "scaAutoPrEnabled":false,
            "webhookId":"555312209",
            "sshRepoUrl":"git@github.com:happy-cook/JavaVulnerableLab.git",
            "sshState":"SKIPPED",
            "isRepoAdmin":true,
            "containerScannerEnabled":true
            }

    Returns:

    {
    'id': '174896',
    'url': 'https://github.com/happy-cook/JavaVulnerableLab',
    'webhookId': '555312209',
    'webhookEnabled': True,
    'prDecorationEnabled': False,
    'isRepoAdmin': True,
    'sastIncrementalScan': True,
    'sastScannerEnabled': True,
    'scaScannerEnabled': True,
    'kicsScannerEnabled': True,
    'apiSecScannerEnabled': True,
    'containerScannerEnabled': True,
    'ossfSecoreCardScannerEnabled': True,
    'secretsDerectionScannerEnabled': True,
    'privatePackage': False,
    'branches': [{'name': 'master', 'isDefaultBranch': True}],
    'sshRepoUrl': 'git@github.com:happy-cook/JavaVulnerableLab.git',
    'scmId': 1,
    'scaAutoPrEnabled': False,
    'kicsAutoPrEnabled': False,
    'sastAutoPrEnabled': False
    }

    """
    relative_url = f"/api/repos-manager/repo/{repo_id}?projectId={project_id}"
    response = put_request(relative_url=relative_url, json=pay_load)
    return response.json()
