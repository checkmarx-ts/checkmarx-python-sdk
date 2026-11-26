from unittest.mock import MagicMock

from CheckmarxPythonSDK.CxOne.repoManagerAPI import (
    RepoImportResult,
    RepoManagerAPI,
)

LINK = "https://example.com/link/abc"
REPO = {
    "id": "4", "name": "java-vulnerable-lab", "url": f"{LINK}/g/java-vulnerable-lab",
    "defaultBranch": "main", "fullName": "g/java-vulnerable-lab",
    "imported": False, "repoAdmin": True, "suggested": False,
    "isRepoAdmin": True, "isSuggested": False, "isImported": False,
    "someFutureField": 1,
}
IMPORT_RESPONSE = {
    "orgConfigResult": {"orgIdentity": "g", "status": "SUCCESS", "statusMessageError": None},
    "repoConfigResultList": [{
        "repoId": 330601, "projectId": "a1f2", "repoIdentity": "4",
        "scmProjectIdentity": None, "repoUrl": REPO["url"], "status": "SUCCESS",
        "statusMessageError": None, "name": "g/java-vulnerable-lab",
        "overriddenSettings": [
            {"field": "ossfScoreCardScannerEnabled", "reason": "UNSUPPORTED_SCM_TYPE"},
            {"field": "aiscScannerEnabled", "reason": "LICENSE"},
        ],
    }],
}


def _api(payload):
    client = MagicMock()
    client.configuration.server_base_url = "https://example.com"
    client.call_api.return_value.json.return_value = payload
    return RepoManagerAPI(api_client=client), client


def test_get_all_repos_for_scm_id_parses_response_and_builds_request():
    api, client = _api({"repos": [REPO]})
    repos = api.get_all_repos_for_scm_id(2577, "g", auth_code="code")
    kwargs = client.call_api.call_args.kwargs
    assert kwargs["url"] == "https://example.com/api/repos-manager/v2/scms/2577/orgs/g/repos"
    assert kwargs["params"] == {"isUser": "false", "authCode": "code"}
    repo = repos.repos[0]
    assert repo.name == "java-vulnerable-lab" and repo.imported is False and repo.repoAdmin is True


def test_token_id_is_sent_instead_of_auth_code():
    api, client = _api({"repos": []})
    api.get_all_repos_for_scm_id(1, "o", token_id="t", is_user=True)
    assert client.call_api.call_args.kwargs["params"] == {"isUser": "true", "tokenId": "t"}


def test_repo_import_for_scm_id_request_and_typed_result():
    api, client = _api(IMPORT_RESPONSE)
    repo_req = {"id": "4", "origin": "GITLAB"}
    result = api.repo_import_for_scm_id(
        2577, "g", [repo_req], auth_code="code",
        create_ast_project=True, scan_ast_project=True,
    )
    kwargs = client.call_api.call_args.kwargs
    assert kwargs["method"] == "POST"
    assert kwargs["url"] == "https://example.com/api/repos-manager/scms/2577/orgs/g/repos"
    assert kwargs["params"] == {
        "isUser": "false", "createAstProject": "true", "scanAstProject": "true",
        "authCode": "code",
    }
    assert kwargs["json"] == {
        "reposFromRequest": [repo_req], "orgSshKey": "", "orgSshState": "SKIPPED",
    }
    assert "headers" not in kwargs
    assert isinstance(result, RepoImportResult)
    assert result.orgConfigResult.status == "SUCCESS"
    r = result.repoConfigResultList[0]
    assert (r.repoId, r.projectId, r.status) == (330601, "a1f2", "SUCCESS")
    assert [o.reason for o in r.overriddenSettings] == ["UNSUPPORTED_SCM_TYPE", "LICENSE"]


def test_import_result_tolerates_empty_lists():
    result = RepoImportResult.from_dict(
        {"orgConfigResult": {"orgIdentity": "g", "status": "FAILED"}}
    )
    assert result.repoConfigResultList == []
