import math
import json
import time
import logging
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from requests.exceptions import ChunkedEncodingError
from requests import Response
from .projectsAPI import get_all_projects

logger = logging.getLogger("CheckmarxPythonSDK")


class RepoManagerAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.origin_dict = {
            "GITHUB": 1,
            "GITLAB": 2,
            "AZURE": 3,
            "BITBUCKET": 4,
        }

    def check_origin(self, origin: str) -> str:
        """

        Args:
            origin (str):

        Returns:
            str
        """
        origin = origin.upper()
        if origin not in self.origin_dict.keys():
            raise ValueError(f"origin {origin} not support! Currently only support GITHUB, GITLAB, AZURE, BITBUCKET")
        return origin

    def get_repos(
            self, origin: str, organization: str, auth_code: str, is_user: bool = False, page: int = 1
    ) -> Response:
        """

        Args:
            origin (str):
            organization (str):
            auth_code (str):
            is_user (bool):
            page (int):

        Returns:
            Response
        """
        origin = self.check_origin(origin)
        relative_url = f"/api/repos-manager/scms/{self.origin_dict.get(origin)}/orgs/{organization}/repos"
        params = {
            "authCode": auth_code,
            "isUser": str(is_user).lower(),
            "page": page,
        }
        return self.api_client.get_request(relative_url=relative_url, params=params)

    def get_all_repos(self, origin: str, organization: str, auth_code: str, is_user: bool = False) -> List[dict]:
        """

        Args:
            origin (str):
            organization (str):
            auth_code (str):
            is_user (bool):

        Returns:
            List[dict]
        """
        origin = self.check_origin(origin)
        result = []
        page = 1
        while True:
            repos = self.get_repos(
                origin=origin, organization=organization, auth_code=auth_code, is_user=is_user, page=page
            ).json().get("repoWebDtoList")
            page += 1
            if not repos:
                break
            result.extend(repos)
        return result

    def get_repo_branches(
            self, origin: str, organization: str, repo_name: str, auth_code: str, page: int = 1
    ) -> Response:
        """

        Args:
            origin (str):
            organization (str):
            repo_name (str):
            auth_code (str):
            page (int):

        Returns:
            Response
        """
        origin = self.check_origin(origin)
        relative_url = (f"/api/repos-manager/scms/{self.origin_dict.get(origin)}/orgs/{organization}/repos"
                        f"/{repo_name}/branches")
        params = {"authCode": auth_code, "page": page}
        return self.api_client.get_request(relative_url=relative_url, params=params)

    def get_all_repo_branches(self, origin: str, organization: str, repo_name: str, auth_code: str) -> List[dict]:
        """

        Args:
            origin (str):
            organization (str):
            repo_name (str):
            auth_code (str):

        Returns:
            List[dict]
        """
        origin = self.check_origin(origin)
        result = []
        page = 1
        while True:
            repos = self.get_repo_branches(
                origin=origin, organization=organization, repo_name=repo_name, auth_code=auth_code, page=page
            ).json().get("branchWebDtoList")
            page += 1
            if not repos:
                break
            result.extend(repos)
        return result

    @staticmethod
    def construct_repo_request(
            http_repo_url: str, ssh_repo_url: str, repo_id: str = None, branches: List[dict] = None,
            is_repo_admin: bool = False, origin: str = "GITHUB", kics_scanner_enabled: bool = True,
            sast_incremental_scan: bool = True, sast_scanner_enabled: bool = True, api_sec_scanner_enabled: bool = True,
            sca_scanner_enabled: bool = True, webhook_enabled: bool = True, pr_decoration_enabled: bool = True,
            sca_auto_pr_enabled: bool = False, container_scanner_enabled: bool = True,
            ossf_score_card_scanner_enabled: bool = True, secrets_detection_scanner_enabled: bool = True,
            project_id: str = None, default_branch: str = None, groups: List[str] = None, 
            private_repository_scan: bool = False, tags: dict = None,
    ) -> dict:
        """

        Args:
            http_repo_url (str):
            ssh_repo_url (str):
            repo_id (str):
            branches (List[dict]): example: [
                    {
                        "name": "master",
                        "isDefaultBranch": True
                    }
                ]
            is_repo_admin (bool):
            origin (str):
            kics_scanner_enabled (bool):
            sast_incremental_scan (bool):
            sast_scanner_enabled (bool):
            api_sec_scanner_enabled (bool):
            sca_scanner_enabled (bool):
            webhook_enabled (bool):
            pr_decoration_enabled (bool):
            sca_auto_pr_enabled (bool):
            container_scanner_enabled (bool):
            ossf_score_card_scanner_enabled (bool):
            secrets_detection_scanner_enabled (bool):
            project_id (str):
            default_branch (str):
            groups (List[str]):
            private_repository_scan (bool):
            tags (dict):

        Returns:
            dict
        """
        http_repo_url = http_repo_url.replace(".git", "")
        org_repo_name = "/".join(http_repo_url.split("/")[3:])
        if origin in ["AZURE", "BITBUCKET"]:
            org_repo_name = "/".join(org_repo_name.split("/")[0:2])
        repo_name = org_repo_name.split("/")[1]
        data = {
            "apiSecScannerEnabled": api_sec_scanner_enabled,
            "branches": branches,
            "containerScannerEnabled": container_scanner_enabled,
            "defaultBranch": default_branch,
            "groups": groups or [],
            "id": repo_name,
            "isRepoAdmin": is_repo_admin,
            "kicsScannerEnabled": kics_scanner_enabled,
            "name": org_repo_name,
            "origin": origin,
            "ossfScoreCardScannerEnabled": ossf_score_card_scanner_enabled,
            "prDecorationEnabled": pr_decoration_enabled,
            "privateRepositoryScan": private_repository_scan,
            "sastIncrementalScan": sast_incremental_scan,
            "sastScannerEnabled": sast_scanner_enabled,
            "scaAutoPrEnabled": sca_auto_pr_enabled,
            "scaScannerEnabled": sca_scanner_enabled,
            "scmRepoId": repo_name,
            "secretsDetectionScannerEnabled": secrets_detection_scanner_enabled,
            "sshState": "SKIPPED",
            "tags": tags,
            "url": http_repo_url,
            "webhookEnabled": webhook_enabled,
        }
        if origin in ['GITLAB', "BITBUCKET"]:
            data.update({"id": repo_id})
        if origin in ["AZURE"]:
            data.update({
                "id": repo_id,
                "projectId": project_id,
            })
        return data

    def repo_import(
            self, origin: str, organization: str, auth_code: str, repos_from_request: List[dict], is_user: bool = False,
            is_org_webhook_enabled: bool = False, create_ast_project: bool = True, scan_ast_project: bool = False
    ) -> Response:
        """

        Args:
            origin (str):
            organization (str):
            auth_code (str):
            repos_from_request (List[dict]):
            is_user (bool):
            is_org_webhook_enabled (bool):
            create_ast_project (bool):
            scan_ast_project (bool):

        Returns:
            Response
        """
        params = {
            "authCode": auth_code,
            "isUser": str(is_user).lower(),
            "isOrgWebhookEnabled": str(is_org_webhook_enabled).lower(),
            "createAstProject": str(create_ast_project).lower(),
            "scanAstProject": str(scan_ast_project).lower()
        }
        logger.debug(f"params: {params}")
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
        logger.debug(f"payload: {data}")
        relative_url = f"/api/repos-manager/scms/{self.origin_dict.get(origin)}/orgs/{organization}/"
        if origin == "GITHUB":
            relative_url += "asyncImport"
        else:
            relative_url += "repos"
        response = self.api_client.post_request(relative_url=relative_url, params=params, headers=headers, json=data)
        return response

    def get_job_status(self) -> int:
        """0 - 100"""
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
        response = self.api_client.get_request(relative_url, headers=headers)
        data_list = [json.loads(item.replace("data:", "")) for item in response.text.split("\n") if item != ""]
        job_percentage = data_list[-1].get("percentage")
        return job_percentage

    def batch_import_repo(
            self, repos: List[dict], origin: str, organization: str, auth_code: str, chunk_size: int = 200,
            is_user: bool = False, is_org_webhook_enabled: bool = False, create_ast_project: bool = True,
            scan_ast_project: bool = False, kics_scanner_enabled: bool = True, sast_incremental_scan: bool = True,
            sast_scanner_enabled: bool = True, api_sec_scanner_enabled: bool = True, sca_scanner_enabled: bool = True,
            webhook_enabled: bool = True, pr_decoration_enabled: bool = True, sca_auto_pr_enabled: bool = False,
            container_scanner_enabled: bool = True, ossf_score_card_scanner_enabled: bool = True,
            secrets_detection_scanner_enabled: bool = True, groups: List[str] = None, 
            private_repository_scan: bool = False, tags: dict = None, is_repo_admin: bool = False,
    ) -> None:
        """

        Args:
            repos (List[dict]):
            origin (str):
            organization (str):
            auth_code (str):
            chunk_size (int):
            is_user (bool):
            is_org_webhook_enabled (bool):
            create_ast_project (bool):
            scan_ast_project (bool):
            kics_scanner_enabled (bool):
            sast_incremental_scan (bool):
            sast_scanner_enabled (bool):
            api_sec_scanner_enabled (bool):
            sca_scanner_enabled (bool):
            webhook_enabled (bool):
            pr_decoration_enabled (bool):
            sca_auto_pr_enabled (bool):
            container_scanner_enabled (bool):
            ossf_score_card_scanner_enabled (bool):
            secrets_detection_scanner_enabled (bool):
            groups (List[str]):
            private_repository_scan (bool):
            tags (dict):
            is_repo_admin (bool):

        Returns:
            None
        """
        origin = self.check_origin(origin)
        project_list = get_all_projects()
        project_name_list = [project.name for project in project_list]
        repo_requests = []
        for repo in repos:
            repo_full_name = repo.get("fullName")
            if repo_full_name in project_name_list:
                logger.info(f"repo {repo_full_name} already exist in cx one, skip!")
                continue
            repo_requests.append(
                self.construct_repo_request(
                    http_repo_url=repo.get("url"),
                    ssh_repo_url=repo.get("sshRepoUrl"),
                    repo_id=repo.get("id"),
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
                    is_repo_admin=is_repo_admin,
                    default_branch=repo.get("defaultBranch"), 
                    groups=groups, 
                    private_repository_scan=private_repository_scan, 
                    tags=tags,
                )
            )
        round_of_requests = math.ceil(len(repos) / chunk_size)
        logger.info(f"there are total {len(repos)} repos in org: {organization}, "
                    f"total {len(repo_requests)} repo requests created, "
                    f"will be {round_of_requests} round_of_requests ")
        round_i = 0
        while round_i < round_of_requests:
            repo_request_chunks = repo_requests[round_i * chunk_size: (round_i + 1) * chunk_size]
            logger.debug(f'All urls in this round of chunks: {"\n".join([item.get("url") for item in repo_request_chunks])} ')
            logger.info(f"round {round_i + 1}, number of repos to create: {len(repo_request_chunks)} ")
            round_i += 1
            self.repo_import(
                origin=origin, organization=organization, auth_code=auth_code, repos_from_request=repo_request_chunks,
                is_user=is_user, is_org_webhook_enabled=is_org_webhook_enabled, create_ast_project=create_ast_project,
                scan_ast_project=scan_ast_project
            )
            percentage = 0
            while percentage < 100:
                try:
                    percentage = self.get_job_status()
                    logger.info(f"import percent: {percentage}")
                    time.sleep(10)
                except ChunkedEncodingError as e:
                    logger.info(f"ChunkedEncodingError: {e}")
                    continue
            time.sleep(10)

    def get_repo_by_id(self, repo_id: int) -> dict:
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
        response = self.api_client.get_request(relative_url)
        return response.json()

    def update_repo_by_id(self, repo_id: int, project_id: str, pay_load: dict) -> dict:
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
        relative_url = f"/api/repos-manager/repo/{repo_id}"
        params = {"projectId": project_id}
        response = self.api_client.put_request(relative_url=relative_url, params=params, json=pay_load)
        return response.json()


def check_origin(origin: str) -> str:
    return RepoManagerAPI().check_origin(origin=origin)


def get_repos(origin: str, organization: str, auth_code: str, is_user: bool = False, page: int = 1) -> Response:
    return RepoManagerAPI().get_repos(
        origin=origin, organization=organization, auth_code=auth_code, is_user=is_user, page=page
    )


def get_all_repos(origin: str, organization: str, auth_code: str, is_user: bool = False) -> List[dict]:
    return RepoManagerAPI().get_all_repos(
        origin=origin, organization=organization, auth_code=auth_code, is_user=is_user
    )


def get_repo_branches(origin: str, organization: str, repo_name: str, auth_code: str, page: int = 1) -> Response:
    return RepoManagerAPI().get_repo_branches(
        origin=origin, organization=organization, repo_name=repo_name, auth_code=auth_code, page=page
    )


def get_all_repo_branches(origin: str, organization: str, repo_name: str, auth_code: str) -> List[dict]:
    return RepoManagerAPI().get_all_repo_branches(
        origin=origin, organization=organization, repo_name=repo_name, auth_code=auth_code
    )


def construct_repo_request(
        http_repo_url: str, ssh_repo_url: str, repo_id: str = None, branches: List[dict] = None,
        is_repo_admin: bool = True,
        origin: str = "GITHUB", kics_scanner_enabled: bool = True, sast_incremental_scan: bool = True,
        sast_scanner_enabled: bool = True, api_sec_scanner_enabled: bool = True, sca_scanner_enabled: bool = True,
        webhook_enabled: bool = True, pr_decoration_enabled: bool = True, sca_auto_pr_enabled: bool = False,
        container_scanner_enabled: bool = True, ossf_score_card_scanner_enabled: bool = True,
        secrets_detection_scanner_enabled: bool = True, project_id: str = None
) -> dict:
    return RepoManagerAPI().construct_repo_request(
        http_repo_url=http_repo_url, ssh_repo_url=ssh_repo_url, repo_id=repo_id, branches=branches,
        is_repo_admin=is_repo_admin,
        origin=origin, kics_scanner_enabled=kics_scanner_enabled, sast_incremental_scan=sast_incremental_scan,
        sast_scanner_enabled=sast_scanner_enabled, api_sec_scanner_enabled=api_sec_scanner_enabled,
        sca_scanner_enabled=sca_scanner_enabled, webhook_enabled=webhook_enabled,
        pr_decoration_enabled=pr_decoration_enabled, sca_auto_pr_enabled=sca_auto_pr_enabled,
        container_scanner_enabled=container_scanner_enabled,
        ossf_score_card_scanner_enabled=ossf_score_card_scanner_enabled,
        secrets_detection_scanner_enabled=secrets_detection_scanner_enabled,
        project_id=project_id,
    )


def repo_import(
        origin: str, organization: str, auth_code: str, repos_from_request: List[dict], is_user: bool = False,
        is_org_webhook_enabled: bool = False, create_ast_project: bool = True, scan_ast_project: bool = False
) -> Response:
    return RepoManagerAPI().repo_import(
        origin=origin, organization=organization, auth_code=auth_code, repos_from_request=repos_from_request,
        is_user=is_user, is_org_webhook_enabled=is_org_webhook_enabled, create_ast_project=create_ast_project,
        scan_ast_project=scan_ast_project
    )


def get_job_status() -> int:
    return RepoManagerAPI().get_job_status()


def batch_import_repo(
        repos: List[dict],
        origin: str,
        organization: str,
        auth_code: str,
        chunk_size: int = 200,
        is_user: bool = False,
        is_org_webhook_enabled: bool = False,
        create_ast_project: bool = True,
        scan_ast_project: bool = False,
        kics_scanner_enabled=True,
        sast_incremental_scan=True,
        sast_scanner_enabled=True,
        api_sec_scanner_enabled=True,
        sca_scanner_enabled=True,
        webhook_enabled=True,
        pr_decoration_enabled=True,
        sca_auto_pr_enabled=False,
        container_scanner_enabled=True,
        ossf_score_card_scanner_enabled=True,
        secrets_detection_scanner_enabled=True
) -> None:
    return RepoManagerAPI().batch_import_repo(
        repos=repos, origin=origin, organization=organization, auth_code=auth_code, chunk_size=chunk_size,
        is_user=is_user, is_org_webhook_enabled=is_org_webhook_enabled, create_ast_project=create_ast_project,
        scan_ast_project=scan_ast_project, kics_scanner_enabled=kics_scanner_enabled,
        sast_incremental_scan=sast_incremental_scan, sast_scanner_enabled=sast_scanner_enabled,
        api_sec_scanner_enabled=api_sec_scanner_enabled, sca_scanner_enabled=sca_scanner_enabled,
        webhook_enabled=webhook_enabled, pr_decoration_enabled=pr_decoration_enabled,
        sca_auto_pr_enabled=sca_auto_pr_enabled, container_scanner_enabled=container_scanner_enabled,
        ossf_score_card_scanner_enabled=ossf_score_card_scanner_enabled,
        secrets_detection_scanner_enabled=secrets_detection_scanner_enabled
    )


def get_repo_by_id(repo_id: int) -> dict:
    return RepoManagerAPI().get_repo_by_id(repo_id=repo_id)


def update_repo_by_id(repo_id: int, project_id: str, pay_load: dict) -> dict:
    return RepoManagerAPI().update_repo_by_id(repo_id=repo_id, project_id=project_id, pay_load=pay_load)
