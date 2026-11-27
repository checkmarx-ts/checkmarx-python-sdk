from unittest.mock import MagicMock

from CheckmarxPythonSDK.CxOne.repoManagerAPI import (
    DefaultRepositorySettings,
    FusionScanConfig,
    RepoOrg,
    RepoManagerAPI,
)


def _setting(value, override=True):
    return {"value": value, "allowOverride": override}


ORG = {
    "id": "happy-gitlab",
    "name": "happy-gitlab",
    "isUser": False,
    "defaultRepositorySettings": {
        "kicsScannerEnabled": _setting(True),
        "sastScannerEnabled": _setting(True),
        "ossfScoreCardScannerEnabled": _setting(False, False),
        "remediationSeverities": _setting([]),
        "prDecorationEnabled": _setting(True),
        "fusionScanConfig": {
            "enabled": True, "llmModel": "opus-4.7", "allowOverride": True,
        },
        "someFutureSetting": _setting(1),
    },
    "someFutureOrgField": "x",
}


def _api(payload):
    api_client = MagicMock()
    api_client.configuration.server_base_url = "https://example.com"
    api_client.call_api.return_value.json.return_value = payload
    return RepoManagerAPI(api_client=api_client), api_client


def test_repo_org_from_dict_parses_settings_and_ignores_unknown_keys():
    org = RepoOrg.from_dict(ORG)
    settings = org.defaultRepositorySettings
    assert isinstance(settings, DefaultRepositorySettings)
    assert settings.sastScannerEnabled.value is True
    assert settings.ossfScoreCardScannerEnabled.allowOverride is False
    assert settings.remediationSeverities.value == []
    assert isinstance(settings.fusionScanConfig, FusionScanConfig)
    assert settings.fusionScanConfig.llmModel == "opus-4.7"
    assert settings.aiscScannerEnabled is None


def test_repo_org_without_settings_still_works():
    org = RepoOrg.from_dict({"id": "a", "name": "a", "isUser": True})
    assert org.defaultRepositorySettings is None and org.isUser is True


def test_get_all_repo_orgs_for_scm_id_uses_given_scm_id():
    api, client = _api({"orgs": [ORG, {"id": "root", "name": "root", "isUser": True}]})
    orgs = api.get_all_repo_orgs_for_scm_id(2577, "code")
    kwargs = client.call_api.call_args.kwargs
    assert kwargs["url"] == "https://example.com/api/repos-manager/v2/scms/2577/user/orgs/config"
    assert kwargs["params"] == {"authCode": "code", "pageSize": 50}
    assert [o.id for o in orgs.orgs] == ["happy-gitlab", "root"]


def test_page_is_sent_only_when_given():
    api, client = _api({"orgs": []})
    api.get_all_repo_orgs_for_scm_id(5, "c", page=2, page_size=10)
    assert client.call_api.call_args.kwargs["params"] == {
        "authCode": "c", "pageSize": 10, "page": 2}


def test_type_based_method_still_delegates():
    api, client = _api({"orgs": [ORG]})
    api.check_origin = lambda o: o.upper()
    assert api.get_all_repo_orgs_for_a_scm_type("gitlab", "c", 1).orgs[0].id == "happy-gitlab"
    assert client.call_api.call_args.kwargs["url"].endswith("/v2/scms/2/user/orgs/config")
