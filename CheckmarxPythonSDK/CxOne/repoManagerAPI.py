import math
import json
import time
import logging
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Iterable, List, Optional
import httpx
from httpx import Response
from dataclasses import dataclass, fields
from .projectsAPI import get_all_projects

logger = logging.getLogger(__name__)


@dataclass
class ScmTypeInfo:
    """An SCM type from GET /api/repos-manager/scm-types, the catalog the UI
    takes ``typeId`` from when registering an SCM (e.g. 2 = GitLab)."""
    id: int = None
    name: str = None
    displayName: str = None
    scope: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScmTypeInfo":
        return cls(**_known_fields(cls, item))


@dataclass
class ScmType:
    id: int = None
    type: str = None
    repoBaseUrl: str = None
    authBaseUrl: str = None
    apiBaseUrl: str = None
    displayName: str = None
    clientId: str = None
    scope: str = None
    instanceName: str = None
    onPrem: bool = False
    appId: str = None
    externalId: str = None


@dataclass
class GithubApp:
    id: int = None
    name: str = None
    slug: str = None
    hasInstallation: bool = False


def _known_fields(cls, item: dict) -> dict:
    """Keep only the keys ``cls`` declares, so new server-side fields never
    crash deserialization."""
    names = {f.name for f in fields(cls)}
    return {k: v for k, v in (item or {}).items() if k in names}


@dataclass
class RepoSetting:
    value: object = None
    allowOverride: bool = None

    @classmethod
    def from_dict(cls, item: dict) -> "RepoSetting":
        return cls(**_known_fields(cls, item))


@dataclass
class FusionScanConfig:
    enabled: bool = None
    llmModel: str = None
    allowOverride: bool = None

    @classmethod
    def from_dict(cls, item: dict) -> "FusionScanConfig":
        return cls(**_known_fields(cls, item))


@dataclass
class DefaultRepositorySettings:
    """Default scan settings of an SCM organization. Each setting is a
    ``RepoSetting`` (value/allowOverride); remediationSeverities has a list
    value and fusionScanConfig has its own shape."""
    kicsScannerEnabled: RepoSetting = None
    sastScannerEnabled: RepoSetting = None
    ossfScoreCardScannerEnabled: RepoSetting = None
    secretsDetectionScannerEnabled: RepoSetting = None
    sastIncrementalScan: RepoSetting = None
    scaScannerEnabled: RepoSetting = None
    apiSecScannerEnabled: RepoSetting = None
    containerScannerEnabled: RepoSetting = None
    aiscScannerEnabled: RepoSetting = None
    prDecorationEnabled: RepoSetting = None
    remediationSeverities: RepoSetting = None
    scaAutoPrEnabled: RepoSetting = None
    commitIdScanTagEnabled: RepoSetting = None
    fusionScanConfig: FusionScanConfig = None

    @classmethod
    def from_dict(cls, item: dict) -> "DefaultRepositorySettings":
        known = _known_fields(cls, item)
        kwargs = {
            k: (FusionScanConfig.from_dict(v) if k == "fusionScanConfig"
                else RepoSetting.from_dict(v))
            for k, v in known.items() if isinstance(v, dict)
        }
        return cls(**kwargs)


@dataclass
class RepoOrg:
    id: str = None
    name: str = None
    isUser: bool = False
    installationTokenId: int = None
    webhookEditable: bool = True
    webhookEnabled: bool = True
    defaultRepositorySettings: DefaultRepositorySettings = None

    @classmethod
    def from_dict(cls, item: dict) -> "RepoOrg":
        known = _known_fields(cls, item)
        settings = known.get("defaultRepositorySettings")
        if isinstance(settings, dict):
            known["defaultRepositorySettings"] = (
                DefaultRepositorySettings.from_dict(settings)
            )
        return cls(**known)


@dataclass
class RepoOrgs:
    orgs: List[RepoOrg] = None


@dataclass
class ScmInstallation:
    installationId: int = None
    tokenId: int = None


@dataclass
class Repo:
    id: str = None
    name: str = None
    url: str = None
    defaultBranch: str = None
    fullName: str = None
    isRepoAdmin: bool = True
    isSuggested: bool = False
    isImported: bool = False
    # duplicates of the is* fields that the server also returns
    imported: bool = False
    repoAdmin: bool = True
    suggested: bool = False

    @classmethod
    def from_dict(cls, item: dict) -> "Repo":
        return cls(**_known_fields(cls, item))


@dataclass
class OrgConfigResult:
    orgIdentity: str = None
    status: str = None
    statusMessageError: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "OrgConfigResult":
        return cls(**_known_fields(cls, item))


@dataclass
class OverriddenSetting:
    """A requested repo setting the server changed, e.g.
    reason UNSUPPORTED_SCM_TYPE or LICENSE."""
    field: str = None
    reason: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "OverriddenSetting":
        return cls(**_known_fields(cls, item))


@dataclass
class RepoConfigResult:
    repoId: int = None
    projectId: str = None
    repoIdentity: str = None
    scmProjectIdentity: str = None
    repoUrl: str = None
    status: str = None
    statusMessageError: str = None
    name: str = None
    overriddenSettings: List[OverriddenSetting] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RepoConfigResult":
        known = _known_fields(cls, item)
        known["overriddenSettings"] = [
            OverriddenSetting.from_dict(o)
            for o in (known.get("overriddenSettings") or [])
        ]
        return cls(**known)


@dataclass
class RepoImportResult:
    """Response of POST /api/repos-manager/scms/{id}/orgs/{org}/repos."""
    orgConfigResult: OrgConfigResult = None
    repoConfigResultList: List[RepoConfigResult] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RepoImportResult":
        return cls(
            orgConfigResult=OrgConfigResult.from_dict(
                item.get("orgConfigResult")
            ),
            repoConfigResultList=[
                RepoConfigResult.from_dict(r)
                for r in (item.get("repoConfigResultList") or [])
            ],
        )


@dataclass
class Repos:
    repos: List[Repo] = None


class RepoManagerAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/repos-manager/scms"
        )
        self.base_url_v2 = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/repos-manager/v2/scms"
        )
        self.origin_dict = {
            "GITHUB": 1,
            "GITLAB": 2,
            "AZURE": 3,
            "BITBUCKET": 4,
        }

    def get_scm_types(self) -> List[ScmTypeInfo]:
        """
        List the SCM types Checkmarx One supports
        (GET /api/repos-manager/scm-types). Use an entry's ``id`` as the
        ``type_id`` of create_oauth_based_scm. Not to be confused with
        get_all_scm_types_v2, which lists the SCM instances registered in
        the tenant.

        Returns:
            List[ScmTypeInfo]
        """
        url = f"{self.base_url.rsplit('/', 1)[0]}/scm-types"
        response = self.api_client.call_api(method="GET", url=url)
        return [ScmTypeInfo.from_dict(item) for item in response.json()]

    def get_all_scm_types_v2(self) -> List[ScmType]:
        """
        get all scm types from CxOne tenant. It may cover GITHUB, GITLAB,
        AZURE, BITBUCKET, its self hosted version, and GITHUBAPP.

        Returns:
            List[ScmType]
        """
        url = self.base_url_v2
        response = self.api_client.call_api(
            method="GET",
            url=url,
        )
        return [ScmType(**item) for item in response.json()]

    def create_oauth_based_scm(
        self,
        type_id: int,
        auth_code: str,
        instance_name: str,
        repo_base_url: str,
        client_id: str,
        client_secret: str,
    ) -> int:
        """
        Register an OAuth-based, self-hosted SCM instance
        (POST /api/repos-manager/scms/oauth-based), e.g. an on-prem GitLab
        reached through a Checkmarx Link.

        Args:
            type_id (int): SCM type id from get_all_scm_types_v2()
                (e.g. 2 for GitLab).
            auth_code (str): OAuth authorization code issued by the SCM.
            instance_name (str): Name for the new SCM instance.
            repo_base_url (str): Base url of the SCM, for a Link-backed
                instance the Link's linkUrl
                (https://<tenant>/link/<link-id>).
            client_id (str): OAuth application id registered in the SCM.
            client_secret (str): OAuth application secret.

        Returns:
            int: the new SCM's id (scmId).
        """
        url = f"{self.base_url}/oauth-based"
        payload = {
            "typeId": type_id,
            "authCode": auth_code,
            "instanceName": instance_name,
            "repoBaseUrl": repo_base_url,
            "clientId": client_id,
            "clientSecret": client_secret,
        }
        response = self.api_client.call_api(
            method="POST", url=url, json=payload
        )
        return response.json().get("scmId")

    def get_verify_status_for_user(
        self,
        origin: str,
        auth_code: str,
    ) -> bool:
        """
        Check if user have access to the scm type

        Returns:
            bool
        """
        origin = self.check_origin(origin)
        origin_index = self.origin_dict.get(origin)
        url = f"{self.base_url}/{origin_index}/user/verify"
        params = {
            "authCode": auth_code,
        }
        response = self.api_client.call_api(
            method="GET",
            url=url,
            params=params,
        )
        return response.json()

    def check_origin(
        self,
        origin: str,
    ) -> str:
        """

        Args:
            origin (str):

        Returns:
            str
        """
        origin = origin.upper()
        all_scm_types = self.get_all_scm_types_v2()
        github_apps = [scm for scm in all_scm_types if scm.type == "githubApp"]
        if github_apps:
            self.origin_dict.update({"GITHUBAPP": github_apps[0].id})
        if origin not in self.origin_dict.keys():
            raise ValueError(
                f"origin {origin} not support!"
                f"Currently only support GITHUB, GITLAB, AZURE, BITBUCKET,"
                f"GITHUBAPP"
            )
        return origin

    def get_github_app_info(
        self,
        auth_code: str,
    ) -> GithubApp:
        """
        get github app information
        """
        origin = self.check_origin("GITHUBAPP")
        origin_index = self.origin_dict.get(origin)
        url = f"{self.base_url}/{origin_index}/github-app-info"
        params = {
            "authCode": auth_code,
        }
        response = self.api_client.call_api(
            method="GET",
            url=url,
            params=params,
        )
        return GithubApp(**response.json())

    def create_token_for_github_app(
        self,
        auth_code: str,
    ) -> bool:
        origin = self.check_origin("GITHUBAPP")
        origin_index = self.origin_dict.get(origin)
        url = f"{self.base_url}/{origin_index}/token"
        params = {
            "authCode": auth_code,
        }
        COOKIE = "apt.sid=AP-JMSS596DXCOP-2-1775181116176-45868282; apt.uid=AP-JMSS596DXCOP-2-1775181116178-82487213.0.2.146d83cb-86cc-463f-8ba3-f6a5625c20e3"
        REFERER = "https://sng.ast.checkmarx.net/applicationsAndProjects/projects?tableConfig=%7B%22search%22%3A%7B%22text%22%3A%22%22%7D%2C%22sorting%22%3A%7B%22columnKey%22%3A%22lastScanDate%22%2C%22order%22%3A%22descend%22%7D%2C%22filters%22%3A%7B%22isDeployed%22%3A%5B%22All%22%5D%7D%2C%22pagination%22%3A%7B%22pageSize%22%3A25%2C%22currentPage%22%3A1%7D%2C%22grouping%22%3A%7B%22groups%22%3A%5B%5D%2C%22groupsState%22%3A%5B%5D%7D%7D"

        headers = {
            "cxorigin": "Integrations MFE",
            "origin": "https://sng.ast.checkmarx.net",
            "cookie": COOKIE,
            "referer": REFERER,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            "sec-fetch-site": "same-origin",
        }
        response = self.api_client.call_api(
            method="POST",
            url=url,
            params=params,
            headers=headers,
        )
        return response.status_code == 200

    def get_all_repo_orgs_for_a_scm_type(
        self,
        origin: str,
        auth_code: str,
        page: int,
        page_size: int = 50,
    ) -> RepoOrgs:
        """
        Get all repository organizations for one scm type

        Returns:
            RepoOrgs
        """
        origin = self.check_origin(origin)
        origin_index = self.origin_dict.get(origin)
        return self.get_all_repo_orgs_for_scm_id(
            scm_id=origin_index,
            auth_code=auth_code,
            page=page,
            page_size=page_size,
        )

    def get_all_repo_orgs_for_scm_id(
        self,
        scm_id: int,
        auth_code: str,
        page: int = None,
        page_size: int = 50,
    ) -> RepoOrgs:
        """
        Get the organizations of one registered SCM instance, addressed by
        its SCM id (GET /api/repos-manager/v2/scms/{scm_id}/user/orgs/config).
        Unlike get_all_repo_orgs_for_a_scm_type this also works for
        self-hosted instances registered with create_oauth_based_scm, whose
        ids are not one of the fixed 1-4.

        Args:
            scm_id (int): id from get_all_scm_types_v2() or the scmId
                returned by create_oauth_based_scm.
            auth_code (str): authorization code / token for the SCM.
            page (int, optional): page number; omitted when None.
            page_size (int): page size. Default: 50

        Returns:
            RepoOrgs
        """
        url = f"{self.base_url_v2}/{scm_id}/user/orgs/config"
        params = {"authCode": auth_code, "pageSize": page_size}
        if page is not None:
            params["page"] = page
        response = self.api_client.call_api(
            method="GET",
            url=url,
            params=params,
        )
        return RepoOrgs(
            orgs=[RepoOrg.from_dict(i) for i in response.json().get("orgs", [])]
        )

    def create_installation_of_scm_on_org(
        self,
        origin: str,
        auth_code: str,
        org_name: str,
    ) -> ScmInstallation:
        """
        create installation of an SCM on a particular organization,
        for example, create a githubapp on a github organization.

        """
        origin = self.check_origin(origin)
        origin_index = self.origin_dict.get(origin)
        url = f"{self.base_url}/{origin_index}/installations"
        params = {
            "authCode": auth_code,
            "org-identity": org_name,
        }
        response = self.api_client.call_api(
            method="POST",
            url=url,
            params=params,
        )
        return ScmInstallation(**response.json())

    def get_all_repos_of_an_org_for_a_scm(
        self, origin: str, org_name: str, token_id: str, is_user: bool = False
    ) -> Repos:
        """
        get all repositories for one organization of a scm type.
        """
        origin = self.check_origin(origin)
        origin_index = self.origin_dict.get(origin)
        return self.get_all_repos_for_scm_id(
            scm_id=origin_index,
            org_name=org_name,
            token_id=token_id,
            is_user=is_user,
        )

    def get_all_repos_for_scm_id(
        self,
        scm_id: int,
        org_name: str,
        auth_code: str = None,
        token_id: str = None,
        is_user: bool = False,
    ) -> Repos:
        """
        Get the repositories of one organization of a registered SCM
        instance (GET /api/repos-manager/v2/scms/{scm_id}/orgs/{org}/repos).
        Works for self-hosted instances whose ids are not the fixed 1-4.

        Args:
            scm_id (int): id from get_all_scm_types_v2() or create_oauth_based_scm.
            org_name (str): organization id/name.
            auth_code (str, optional): authorization code for the SCM.
            token_id (str, optional): stored token id, alternative to auth_code.
            is_user (bool): True when org_name is a user namespace.

        Returns:
            Repos
        """
        url = f"{self.base_url_v2}/{scm_id}/orgs/{org_name}/repos"
        params = {"isUser": str(is_user).lower()}
        if auth_code is not None:
            params["authCode"] = auth_code
        if token_id is not None:
            params["tokenId"] = token_id
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return Repos(
            repos=[Repo.from_dict(i) for i in response.json().get("repos", [])]
        )

    def repo_import_for_scm_id(
        self,
        scm_id: int,
        organization: str,
        repos_from_request: List[dict],
        auth_code: str = None,
        token_id: str = None,
        is_user: bool = False,
        is_org_webhook_enabled: bool = None,
        create_ast_project: bool = True,
        scan_ast_project: bool = False,
        org_ssh_key: str = "",
        org_ssh_state: str = "SKIPPED",
    ) -> RepoImportResult:
        """
        Import repositories of one organization of a registered SCM instance
        (POST /api/repos-manager/scms/{scm_id}/orgs/{org}/repos), optionally
        creating and scanning the Checkmarx One projects.

        Args:
            scm_id (int): id of the SCM instance (any registered scm).
            organization (str): organization id/name.
            repos_from_request (List[dict]): repo objects as the UI sends
                them (id, uid, url, scmRepoId, name, origin, defaultBranch,
                branches, scanner flags, sshState, criticality, ...).
            auth_code (str, optional): authorization code for the SCM.
            token_id (str, optional): stored token id.
            is_user (bool): True when organization is a user namespace.
            is_org_webhook_enabled (bool, optional): sent only when given.
            create_ast_project (bool): create the CxOne project.
            scan_ast_project (bool): start a scan after creating it.

        Returns:
            RepoImportResult: org status and a per-repo result, including
            any settings the server overrode (overriddenSettings).
        """
        url = f"{self.base_url}/{scm_id}/orgs/{organization}/repos"
        params = {
            "isUser": str(is_user).lower(),
            "createAstProject": str(create_ast_project).lower(),
            "scanAstProject": str(scan_ast_project).lower(),
        }
        if auth_code is not None:
            params["authCode"] = auth_code
        if token_id is not None:
            params["tokenId"] = token_id
        if is_org_webhook_enabled is not None:
            params["isOrgWebhookEnabled"] = str(is_org_webhook_enabled).lower()
        payload = {
            "reposFromRequest": repos_from_request,
            "orgSshKey": org_ssh_key,
            "orgSshState": org_ssh_state,
        }
        response = self.api_client.call_api(
            method="POST", url=url, params=params, json=payload
        )
        return RepoImportResult.from_dict(response.json())

    def get_repos(
        self,
        origin: str,
        organization: str,
        auth_code: str,
        is_user: bool = False,
        page: int = 1,
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
        origin_index = self.origin_dict.get(origin)
        url = f"{self.base_url}/{origin_index}/orgs/{organization}/repos"
        params = {
            "authCode": auth_code,
            "isUser": str(is_user).lower(),
            "page": page,
        }
        return self.api_client.call_api(
            method="GET", url=url, params=params
        )

    def get_all_repos(
        self,
        origin: str,
        organization: str,
        auth_code: str,
        is_user: bool = False,
    ) -> List[dict]:
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
            repos = (
                self.get_repos(
                    origin=origin,
                    organization=organization,
                    auth_code=auth_code,
                    is_user=is_user,
                    page=page,
                )
                .json()
                .get("repoWebDtoList")
            )
            page += 1
            if not repos:
                break
            result.extend(repos)
        return result

    def get_repo_branches(
        self,
        origin: str,
        organization: str,
        repo_name: str,
        auth_code: str,
        page: int = 1,
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
        origin_index = self.origin_dict.get(origin)
        url = (
            f"{self.base_url}/{origin_index}/orgs/{organization}"
            f"/repos/{repo_name}/branches"
        )
        params = {"authCode": auth_code, "page": page}
        return self.api_client.call_api(
            method="GET", url=url, params=params
        )

    def get_all_repo_branches(
        self, origin: str, organization: str, repo_name: str, auth_code: str
    ) -> List[dict]:
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
            repos = (
                self.get_repo_branches(
                    origin=origin,
                    organization=organization,
                    repo_name=repo_name,
                    auth_code=auth_code,
                    page=page,
                )
                .json()
                .get("branchWebDtoList")
            )
            page += 1
            if not repos:
                break
            result.extend(repos)
        return result

    @staticmethod
    def construct_repo_request(
        http_repo_url: str,
        repo_id: str = None,
        branches: List[dict] = None,
        is_repo_admin: bool = False,
        origin: str = "GITHUB",
        kics_scanner_enabled: bool = True,
        sast_incremental_scan: bool = True,
        sast_scanner_enabled: bool = True,
        api_sec_scanner_enabled: bool = True,
        sca_scanner_enabled: bool = True,
        webhook_enabled: bool = True,
        pr_decoration_enabled: bool = True,
        sca_auto_pr_enabled: bool = False,
        container_scanner_enabled: bool = True,
        ossf_score_card_scanner_enabled: bool = True,
        secrets_detection_scanner_enabled: bool = True,
        project_id: str = None,
        default_branch: str = None,
        groups: List[str] = None,
        private_repository_scan: bool = False,
        tags: dict = None,
    ) -> dict:
        """

        Args:
            http_repo_url (str):
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
        if origin in ["GITLAB", "BITBUCKET"]:
            data.update({"id": repo_id})
        if origin in ["AZURE"]:
            data.update(
                {
                    "id": repo_id,
                    "projectId": project_id,
                }
            )
        return data

    def repo_import(
        self,
        origin: str,
        organization: str,
        auth_code: str = None,
        token_id: str = None,
        repos_from_request: List[dict] = None,
        is_user: bool = False,
        is_org_webhook_enabled: bool = False,
        create_ast_project: bool = True,
        scan_ast_project: bool = False,
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
        scm_id = self.origin_dict.get(origin)
        url = f"{self.base_url}/{scm_id}/orgs/{organization}/"
        if origin in ["GITHUB", "GITHUBAPP"]:
            url += "asyncImport"
        else:
            url += "repos"
        params = {
            "authCode": auth_code,
            "tokenId": token_id,
            "isUser": str(is_user).lower(),
            "isOrgWebhookEnabled": str(is_org_webhook_enabled).lower(),
            "createAstProject": str(create_ast_project).lower(),
            "scanAstProject": str(scan_ast_project).lower(),
        }
        logger.debug(f"params: {params}")
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "sec-ch-ua": (
                '"Chromium";v="134", '
                '"Not:A-Brand";v="24", '
                '"Google Chrome";v="134"'
            ),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "strict-transport-security": "max-age=31536000; includeSubDomains",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/134.0.0.0 Safari/537.36"
            ),
            "webapp": "true",
            "Accept-Encoding": "identity",
        }
        data = {
            "reposFromRequest": repos_from_request,
            "orgSshKey": "",
            "orgSshState": "SKIPPED",
        }
        logger.debug(f"payload: {data}")
        response = self.api_client.call_api(
            method="POST", url=url, params=params, headers=headers, json=data
        )
        return response

    @staticmethod
    def _parse_job_percentage(text: str) -> Optional[int]:
        """Last ``percentage`` in an SSE body, or None when there is none.

        Only ``data:`` lines are read; keep-alive comments, ``event:`` lines
        and malformed payloads are ignored.
        """
        percentage = None
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("data:"):
                continue
            try:
                event = json.loads(line[len("data:"):])
            except ValueError:
                continue
            if isinstance(event, dict) and event.get("percentage") is not None:
                percentage = event["percentage"]
        return percentage

    def get_job_status(self) -> Optional[int]:
        """
        Progress of the running import job (GET /api/ssegateway/job-status,
        a server-sent-events stream).

        Returns:
            int | None: 0 - 100, or None when the stream carried no progress
            event (for example no job is running or none has reported yet).
        """
        url = (
            f"{self.api_client.configuration.server_base_url}"
            "/api/ssegateway/job-status"
        )
        headers = {"accept": "*/*", "Accept-Encoding": "identity"}
        response = self.api_client.call_api(
            method="GET", url=url, headers=headers
        )
        return self._parse_job_percentage(response.text)

    def batch_import_repo(
        self,
        repos: List[dict],
        origin: str,
        organization: str,
        auth_code: str,
        chunk_size: int = 200,
        is_user: bool = False,
        is_org_webhook_enabled: bool = False,
        create_ast_project: bool = True,
        scan_ast_project: bool = False,
        kics_scanner_enabled: bool = True,
        sast_incremental_scan: bool = True,
        sast_scanner_enabled: bool = True,
        api_sec_scanner_enabled: bool = True,
        sca_scanner_enabled: bool = True,
        webhook_enabled: bool = True,
        pr_decoration_enabled: bool = True,
        sca_auto_pr_enabled: bool = False,
        container_scanner_enabled: bool = True,
        ossf_score_card_scanner_enabled: bool = True,
        secrets_detection_scanner_enabled: bool = True,
        groups: List[str] = None,
        private_repository_scan: bool = False,
        tags: dict = None,
        is_repo_admin: bool = False,
        delay_request_timeout: int = 30,
        max_wait_per_round: int = 7200,
        existing_project_names: Optional[Iterable[str]] = None,
    ) -> None:
        """

        Args:
            existing_project_names (Iterable[str]): names of projects that already
                exist in CxOne; repos whose fullName is in it are skipped. When
                None (default) all projects are listed once per call. Pass it
                when calling this method repeatedly (e.g. once per group) so the
                full project list is not fetched again every time.
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
            max_wait_per_round (int): maximum seconds to wait for each import
                round to reach 100% before raising TimeoutError.
            delay_request_timeout (int):

        Returns:
            None
        """
        origin = self.check_origin(origin)
        token_id = None
        if origin == "GITHUBAPP":
            installation = self.create_installation_of_scm_on_org(
                origin="GITHUBAPP",
                auth_code=auth_code,
                org_name=organization,
            )
            token_id = installation.tokenId
            auth_code = None
        if existing_project_names is None:
            existing_project_names = [p.name for p in get_all_projects()]
        project_name_list = set(existing_project_names)
        repo_requests = []
        for repo in repos:
            repo_full_name = repo.get("fullName")
            if repo_full_name in project_name_list:
                logger.info(f"repo {repo_full_name} already exist in cx one, skip!")
                continue
            repo_requests.append(
                self.construct_repo_request(
                    http_repo_url=repo.get("url"),
                    repo_id=repo.get("id"),
                    branches=[
                        {"pattern": repo.get("defaultBranch"), "isDefaultBranch": True}
                    ],
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
        round_of_requests = math.ceil(len(repo_requests) / chunk_size)
        logger.info(
            f"there are total {len(repos)} repos in org: {organization}, "
            f"total {len(repo_requests)} repo requests created, "
            f"will be {round_of_requests} round_of_requests "
        )
        round_i = 0
        while round_i < round_of_requests:
            repo_request_chunks = repo_requests[
                round_i * chunk_size : (round_i + 1) * chunk_size
            ]
            urls_str = "\n".join([item.get("url") for item in repo_request_chunks])
            logger.debug(f"All urls in this round of chunks: {urls_str}")
            logger.info(
                f"round {round_i + 1}, number of repos to create: "
                f"{len(repo_request_chunks)} "
            )
            round_i += 1
            self.repo_import(
                origin=origin,
                organization=organization,
                auth_code=auth_code,
                token_id=token_id,
                repos_from_request=repo_request_chunks,
                is_user=is_user,
                is_org_webhook_enabled=is_org_webhook_enabled,
                create_ast_project=create_ast_project,
                scan_ast_project=scan_ast_project,
            )
            percentage = 0
            deadline = time.monotonic() + max_wait_per_round
            while percentage < 100:
                if time.monotonic() >= deadline:
                    raise TimeoutError(
                        f"repo import round {round_i} did not finish within "
                        f"{max_wait_per_round}s, last percent: {percentage}"
                    )
                try:
                    status = self.get_job_status()
                    if status is not None:
                        percentage = status
                    logger.info(f"import percent: {percentage}")
                except httpx.RemoteProtocolError as e:
                    logger.info(f"ChunkedEncodingError: {e}")
                time.sleep(delay_request_timeout)
            time.sleep(delay_request_timeout)

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

        url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/repos-manager/repo/{repo_id}"
        )
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def scm_managed_project_scan(
        self,
        project_id: str,
        origin: str,
        organization: str,
        repo_id: int,
        repo_identity: str,
        repo_url: str,
        default_branch: str,
        scanner_types: List[str] = None,
        is_incremental_scan: bool = False,
        org_ssh_key: str = None,
    ) -> Response:
        """Trigger a new scan for an existing CxOne project via its registered
        SCM connection.

        This wraps the repos-manager projectScan endpoint
        (``POST /api/repos-manager/scms/{scm_id}/orgs/{organization}/repo/projectScan``),
        which is distinct from ``create_scan`` from ``scansAPI``:

        * ``create_scan`` requires the caller to supply source material
          (file path, zip, or git URL) and is used for ad-hoc / standalone
          scans.
        * ``scm_managed_project_scan`` instructs CxOne to pull source from
          the SCM connection already registered for the project; it's the
          right entry point when automating "rescan an existing project on
          its primary branch."

        Args:
            project_id (str): CxOne project UUID.
            origin (str): SCM origin, one of GITHUB, GITLAB, AZURE, BITBUCKET.
            organization (str): SCM organization slug (the org under which
                the repo lives within the SCM).
            repo_id (int): CxOne-internal repo ID. Available from project
                metadata under ``repoId``.
            repo_identity (str): SCM-side repo identifier. Available from
                project metadata under ``scmRepoId``.
            repo_url (str): Repository URL.
            default_branch (str): Branch to scan (typically the project's
                ``mainBranch``).
            scanner_types (List[str]): Engines to run. Defaults to the full
                set: ``["sast", "sca", "kics", "apisec", "containers", "2ms"]``.
            is_incremental_scan (bool): Request incremental SAST. Defaults
                to False (full scan).
            org_ssh_key (str): Optional SSH key for the SCM connection.
                Defaults to None.

        Returns:
            Response: HTTP response from the projectScan endpoint. CxOne
            typically returns 2xx with an empty body on accept; the scan
            shows up shortly after in ``get_a_list_of_scans``.

        Raises:
            ValueError: If ``origin`` is not a supported SCM type.

        Example::

            from CheckmarxPythonSDK.CxOne import (
                RepoManagerAPI, get_a_project_by_id,
            )
            project = get_a_project_by_id(project_id="<uuid>")
            RepoManagerAPI().scm_managed_project_scan(
                project_id=project["id"],
                origin=project["origin"],
                organization="<scm-org-slug>",
                repo_id=project["repoId"],
                repo_identity=project["scmRepoId"],
                repo_url=project["repoUrl"],
                default_branch=project["mainBranch"],
            )
        """
        scm_id = self.origin_dict.get(origin.upper())
        if scm_id is None:
            raise ValueError(
                f"Unsupported origin '{origin}'. "
                f"Supported: {list(self.origin_dict.keys())}"
            )
        if scanner_types is None:
            scanner_types = [
                "sast", "sca", "kics", "apisec", "containers", "2ms",
            ]

        url = (
            f"{self.base_url}/{scm_id}/orgs/{organization}"
            f"/repo/projectScan"
        )
        params = {"projectId": project_id}
        payload = {
            "repoOrigin": origin.lower(),
            "project": {
                "repoIdentity": str(repo_identity),
                "repoUrl": repo_url,
                "projectId": project_id,
                "defaultBranch": default_branch,
                "scannerTypes": scanner_types,
                "repoId": str(repo_id),
                "isIncrementalScan": is_incremental_scan,
            },
            "orgSshKey": org_ssh_key,
        }
        response = self.api_client.call_api(
            method="POST", url=url, params=params, json=payload
        )
        return response

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
        url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/repos-manager/repo/{repo_id}"
        )
        params = {"projectId": project_id}
        response = self.api_client.call_api(
            method="PUT", url=url, params=params, json=pay_load
        )
        return response.json()


def check_origin(origin: str) -> str:
    return RepoManagerAPI().check_origin(origin=origin)


def get_repos(
    origin: str, organization: str, auth_code: str, is_user: bool = False, page: int = 1
) -> Response:
    return RepoManagerAPI().get_repos(
        origin=origin,
        organization=organization,
        auth_code=auth_code,
        is_user=is_user,
        page=page,
    )


def get_all_repos(
    origin: str, organization: str, auth_code: str, is_user: bool = False
) -> List[dict]:
    return RepoManagerAPI().get_all_repos(
        origin=origin, organization=organization, auth_code=auth_code, is_user=is_user
    )


def get_repo_branches(
    origin: str, organization: str, repo_name: str, auth_code: str, page: int = 1
) -> Response:
    return RepoManagerAPI().get_repo_branches(
        origin=origin,
        organization=organization,
        repo_name=repo_name,
        auth_code=auth_code,
        page=page,
    )


def get_all_repo_branches(
    origin: str, organization: str, repo_name: str, auth_code: str
) -> List[dict]:
    return RepoManagerAPI().get_all_repo_branches(
        origin=origin,
        organization=organization,
        repo_name=repo_name,
        auth_code=auth_code,
    )


def construct_repo_request(
    http_repo_url: str,
    repo_id: str = None,
    branches: List[dict] = None,
    is_repo_admin: bool = True,
    origin: str = "GITHUB",
    kics_scanner_enabled: bool = True,
    sast_incremental_scan: bool = True,
    sast_scanner_enabled: bool = True,
    api_sec_scanner_enabled: bool = True,
    sca_scanner_enabled: bool = True,
    webhook_enabled: bool = True,
    pr_decoration_enabled: bool = True,
    sca_auto_pr_enabled: bool = False,
    container_scanner_enabled: bool = True,
    ossf_score_card_scanner_enabled: bool = True,
    secrets_detection_scanner_enabled: bool = True,
    project_id: str = None,
    default_branch: str = None,
    groups: List[str] = None,
    private_repository_scan: bool = False,
    tags: dict = None,
) -> dict:
    return RepoManagerAPI().construct_repo_request(
        http_repo_url=http_repo_url,
        repo_id=repo_id,
        branches=branches,
        is_repo_admin=is_repo_admin,
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
        project_id=project_id,
        default_branch=default_branch,
        groups=groups,
        private_repository_scan=private_repository_scan,
        tags=tags,
    )


def repo_import(
    origin: str,
    organization: str,
    auth_code: str,
    token_id: str = None,
    repos_from_request: List[dict] = None,
    is_user: bool = False,
    is_org_webhook_enabled: bool = False,
    create_ast_project: bool = True,
    scan_ast_project: bool = False,
) -> Response:
    return RepoManagerAPI().repo_import(
        origin=origin,
        organization=organization,
        auth_code=auth_code,
        token_id=token_id,
        repos_from_request=repos_from_request,
        is_user=is_user,
        is_org_webhook_enabled=is_org_webhook_enabled,
        create_ast_project=create_ast_project,
        scan_ast_project=scan_ast_project,
    )


def get_job_status() -> Optional[int]:
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
    secrets_detection_scanner_enabled=True,
    groups: List[str] = None,
    private_repository_scan: bool = False,
    tags: dict = None,
    is_repo_admin: bool = False,
    delay_request_timeout: int = 30,
    max_wait_per_round: int = 7200,
    existing_project_names: Optional[Iterable[str]] = None,
) -> None:
    return RepoManagerAPI().batch_import_repo(
        repos=repos,
        origin=origin,
        organization=organization,
        auth_code=auth_code,
        chunk_size=chunk_size,
        is_user=is_user,
        is_org_webhook_enabled=is_org_webhook_enabled,
        create_ast_project=create_ast_project,
        scan_ast_project=scan_ast_project,
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
        groups=groups,
        private_repository_scan=private_repository_scan,
        tags=tags,
        is_repo_admin=is_repo_admin,
        delay_request_timeout=delay_request_timeout,
        max_wait_per_round=max_wait_per_round,
        existing_project_names=existing_project_names,
    )


def get_repo_by_id(repo_id: int) -> dict:
    return RepoManagerAPI().get_repo_by_id(repo_id=repo_id)


def update_repo_by_id(repo_id: int, project_id: str, pay_load: dict) -> dict:
    return RepoManagerAPI().update_repo_by_id(
        repo_id=repo_id, project_id=project_id, pay_load=pay_load
    )


def scm_managed_project_scan(
    project_id: str,
    origin: str,
    organization: str,
    repo_id: int,
    repo_identity: str,
    repo_url: str,
    default_branch: str,
    scanner_types: List[str] = None,
    is_incremental_scan: bool = False,
    org_ssh_key: str = None,
) -> Response:
    return RepoManagerAPI().scm_managed_project_scan(
        project_id=project_id,
        origin=origin,
        organization=organization,
        repo_id=repo_id,
        repo_identity=repo_identity,
        repo_url=repo_url,
        default_branch=default_branch,
        scanner_types=scanner_types,
        is_incremental_scan=is_incremental_scan,
        org_ssh_key=org_ssh_key,
    )


def create_oauth_based_scm(
    type_id: int,
    auth_code: str,
    instance_name: str,
    repo_base_url: str,
    client_id: str,
    client_secret: str,
) -> int:
    return RepoManagerAPI().create_oauth_based_scm(
        type_id=type_id,
        auth_code=auth_code,
        instance_name=instance_name,
        repo_base_url=repo_base_url,
        client_id=client_id,
        client_secret=client_secret,
    )


def get_scm_types() -> List[ScmTypeInfo]:
    return RepoManagerAPI().get_scm_types()
