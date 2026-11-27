from unittest.mock import MagicMock

from CheckmarxPythonSDK.CxOne import get_orgs_coverage  # noqa: F401
from CheckmarxPythonSDK.CxOne.discoveryAPI import DiscoveryAPI
from CheckmarxPythonSDK.CxOne.dto import OrgCoverage, ScmCoverage

PAYLOAD = [
    {
        "totalReposCount": 44, "totalImportedReposCount": 4, "totalKpiNumber": 9,
        "scmId": 1, "type": "github", "display": "YES", "onPrem": False,
        "orgCoverageDtoList": [
            {"orgId": 11122, "orgIdentity": "cx-happy-yang", "scmId": 1,
             "reposCount": 41, "importedReposCount": 2, "kpiNumber": 4.0,
             "adminToken": False},
            {"orgId": 10165, "orgIdentity": "happy-cook", "scmId": 1,
             "reposCount": 3, "importedReposCount": 2, "kpiNumber": 66.0,
             "adminToken": False, "someFutureField": 1},
        ],
    },
    {
        "totalReposCount": 3, "totalImportedReposCount": 1, "totalKpiNumber": 33,
        "scmId": 2577, "type": "gitlab", "display": "YES", "onPrem": True,
        "orgCoverageDtoList": [
            {"orgId": 12059, "orgIdentity": "happy-gitlab", "scmId": 2577,
             "reposCount": 3, "importedReposCount": 1, "kpiNumber": 33.0,
             "adminToken": False},
        ],
    },
]


def _api(payload):
    client = MagicMock()
    client.configuration.server_base_url = "https://example.com"
    client.call_api.return_value.json.return_value = payload
    return DiscoveryAPI(api_client=client), client


def test_get_orgs_coverage_request_and_parsing():
    api, client = _api(PAYLOAD)
    result = api.get_orgs_coverage()
    kwargs = client.call_api.call_args.kwargs
    assert kwargs["method"] == "GET"
    assert kwargs["url"] == "https://example.com/api/discovery/v2/orgs/coverage"
    assert [s.scm_id for s in result] == [1, 2577]
    gitlab = result[1]
    assert isinstance(gitlab, ScmCoverage)
    assert (gitlab.type, gitlab.on_prem, gitlab.total_repos_count) == ("gitlab", True, 3)
    assert gitlab.total_imported_repos_count == 1 and gitlab.total_kpi_number == 33
    org = gitlab.org_coverage_list[0]
    assert isinstance(org, OrgCoverage)
    assert (org.org_identity, org.org_id, org.imported_repos_count) == ("happy-gitlab", 12059, 1)
    assert org.kpi_number == 33.0 and org.admin_token is False
    assert len(result[0].org_coverage_list) == 2


def test_empty_and_missing_org_list():
    api, _ = _api([{"scmId": 9}])
    assert api.get_orgs_coverage()[0].org_coverage_list == []
    api, _ = _api([])
    assert api.get_orgs_coverage() == []
