from unittest.mock import MagicMock

from CheckmarxPythonSDK.CxOne.cxLinkAPI import CxLinkAPI
from CheckmarxPythonSDK.CxOne.dto import CxLink

SAMPLE = {
    "id": "539e491d-5190-4021-b949-40d5b3c891da",
    "name": "local_gitlab",
    "description": "",
    "privateUrl": "https://gitlab.happy.local/",
    "linkUrl": "https://sng.ast.checkmarx.net/link/539e491d-5190-4021-b949-40d5b3c891da",
    "state": "connected",
    "clientType": "docker",
    "clientVersion": "2.3.0",
    "clientPrivateUrl": "https://gitlab.happy.local",
    "createdAt": "2026-11-26T07:04:05.880458Z",
}


def test_from_dict_maps_all_fields():
    link = CxLink.from_dict(SAMPLE)
    assert link.id == SAMPLE["id"]
    assert link.private_url == "https://gitlab.happy.local/"
    assert link.link_url.endswith(SAMPLE["id"])
    assert (link.state, link.client_type, link.client_version) == ("connected", "docker", "2.3.0")
    assert link.client_private_url == "https://gitlab.happy.local"
    assert link.created_at == SAMPLE["createdAt"]


def test_from_dict_tolerates_missing_fields():
    assert CxLink.from_dict({"id": "x"}).name is None


def test_get_link_returns_cxlink():
    api_client = MagicMock()
    api_client.configuration.server_base_url = "https://example.com"
    api_client.call_api.return_value.json.return_value = SAMPLE
    link = CxLinkAPI(api_client=api_client).get_link(SAMPLE["id"])
    assert isinstance(link, CxLink) and link.name == "local_gitlab"
