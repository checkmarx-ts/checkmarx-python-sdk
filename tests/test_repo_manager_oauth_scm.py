from unittest.mock import MagicMock

from CheckmarxPythonSDK.CxOne import create_oauth_based_scm  # noqa: F401
from CheckmarxPythonSDK.CxOne.repoManagerAPI import RepoManagerAPI


def test_create_oauth_based_scm_posts_expected_payload():
    api_client = MagicMock()
    api_client.configuration.server_base_url = "https://example.com"
    api_client.call_api.return_value.json.return_value = {"scmId": 2577}

    scm_id = RepoManagerAPI(api_client=api_client).create_oauth_based_scm(
        type_id=2,
        auth_code="code",
        instance_name="gitlab_x",
        repo_base_url="https://example.com/link/abc",
        client_id="cid",
        client_secret="secret",
    )

    assert scm_id == 2577
    kwargs = api_client.call_api.call_args.kwargs
    assert kwargs["method"] == "POST"
    assert kwargs["url"] == "https://example.com/api/repos-manager/scms/oauth-based"
    assert kwargs["json"] == {
        "typeId": 2,
        "authCode": "code",
        "instanceName": "gitlab_x",
        "repoBaseUrl": "https://example.com/link/abc",
        "clientId": "cid",
        "clientSecret": "secret",
    }
