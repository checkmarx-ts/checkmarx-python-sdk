"""DAST Results Service REST API (stubs).

Endpoints under <server>/api/dast/mfe-results. Methods return raw
response.json() (or response.text) until each endpoint's response
shape is pinned down and we add DTOs — same approach we took for
dastScanAPI before typing it endpoint-by-endpoint.
"""
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class DastResultsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/dast/mfe-results"
        )

    def get_results(self, scan_id: str, **params) -> dict:
        """GET /results/{scan_id} — information about results (risks)
        identified by a specific DAST scan."""
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/results/{scan_id}",
            params=params,
        )
        return response.json()

    def update_results(self, changelog: dict) -> dict:
        """POST /changelog — edit severity/comments/state on one or
        more results (single or batch)."""
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/changelog", json=changelog,
        )
        return response.json()

    def get_result_info(self, result_id: str, scan_id: str) -> dict:
        """GET /results/info/{result_id}/{scan_id} — detailed info
        about a specific result on a specific scan."""
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/info/{result_id}/{scan_id}",
        )
        return response.json()

    def get_results_count_by_group(self, scan_id: str, **params) -> dict:
        """GET /results/{scan_id}/group — count of results per group
        on a specific scan."""
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/results/{scan_id}/group",
            params=params,
        )
        return response.json()


# ----- Module-level conveniences -----

def get_results(scan_id: str, **params) -> dict:
    return DastResultsAPI().get_results(scan_id=scan_id, **params)


def update_results(changelog: dict) -> dict:
    return DastResultsAPI().update_results(changelog=changelog)


def get_result_info(result_id: str, scan_id: str) -> dict:
    return DastResultsAPI().get_result_info(result_id=result_id, scan_id=scan_id)


def get_results_count_by_group(scan_id: str, **params) -> dict:
    return DastResultsAPI().get_results_count_by_group(scan_id=scan_id, **params)
