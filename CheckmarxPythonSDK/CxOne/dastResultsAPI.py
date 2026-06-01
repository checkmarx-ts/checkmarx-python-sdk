"""DAST Results Service REST API.

Endpoints under <server>/api/dast/mfe-results. Endpoints with
documented response shapes return DTO objects; the rest are stubs
that return the raw parsed JSON response until their schemas are
pinned down.
"""
from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    DastResultDetail,
    DastResultsChangelogInput,
    DastResultsCollection,
    DastResultsFilter,
    DastResultsSortBy,
)


def _flatten_filter(name: str, obj_filter) -> dict:
    """Expand a filter DTO into bracketed nested query params
    (e.g. filter[severity]=HIGH) — the wire format the DAST APIs use."""
    if obj_filter is None:
        return {}
    return {f"{name}[{k}]": v for k, v in obj_filter.to_dict().items()}


class DastResultsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/dast/mfe-results"
        )

    def get_results(
        self,
        scan_id: str,
        filter_: DastResultsFilter = None,
        page: int = None,
        per_page: int = None,
        search: str = None,
        sort_by: List[DastResultsSortBy] = None,
        group: str = None,
    ) -> DastResultsCollection:
        """GET /results/{scan_id} — paged results (risks) identified by
        a specific DAST scan.

        Args:
            scan_id (str): UUID of the scan.
            filter_ (DastResultsFilter, optional): partial-match filter
                on severity, path, name, method, status, state, url,
                owasp, alert_similarity_id.
            page (int, optional): 1-based page number. Default 1.
            per_page (int, optional): page size, 1-100. Default 10.
            search (str, optional): substring search across multiple
                columns.
            sort_by (list of DastResultsSortBy, optional): sort columns.
                Each entry is serialized as "<col>:asc"; pass a raw
                "col:desc" string for per-column descending order.
            group (str, optional): filter by groups.

        Returns:
            DastResultsCollection
        """
        params = {
            "page": page,
            "per_page": per_page,
            "search": search,
            "sort_by": (
                [s if ":" in str(s) else f"{s.value if isinstance(s, DastResultsSortBy) else s}:asc"
                 for s in sort_by]
                if sort_by else None
            ),
            "group": group,
        }
        params.update(_flatten_filter("filter", filter_))
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/results/{scan_id}",
            params=params,
        )
        return DastResultsCollection.from_dict(response.json())

    def update_results(self, changelog: DastResultsChangelogInput) -> bool:
        """POST /changelog — update severity/state/notes on one or more
        results (single or batch).

        Args:
            changelog (DastResultsChangelogInput): the update payload.
                similarity_id_2 / environment_id / scan_id are required;
                severity / state / note / type / alert_similarity_id /
                custom_state_id are optional. When type=ALERT,
                alert_similarity_id is required.

        Returns:
            bool: True if the API returned a 2xx status. Response body
            is plain-text "OK" on success.
        """
        response = self.api_client.call_api(
            method="POST", url=f"{self.base_url}/changelog",
            json=changelog.to_dict(),
        )
        return 200 <= response.status_code < 300

    def get_result_info(self, result_id: str, scan_id: str) -> DastResultDetail:
        """GET /results/info/{result_id}/{scan_id} — detailed info about
        a specific result.

        Doc shows the response wrapped as {"results": {...}}, but live
        returns the fields at the top level. Unwraps defensively in
        case the API ever matches the doc.

        Args:
            result_id (str): UUID of the result.
            scan_id (str): UUID of the scan it belongs to.

        Returns:
            DastResultDetail
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/results/info/{result_id}/{scan_id}",
        )
        data = response.json()
        # Doc says wrapped under "results"; live returns flat. Handle both.
        if isinstance(data, dict) and isinstance(data.get("results"), dict):
            data = data["results"]
        return DastResultDetail.from_dict(data)

    def get_results_count_by_group(self, scan_id: str, **params) -> dict:
        """GET /results/{scan_id}/group — count of results per group
        on a specific scan."""
        response = self.api_client.call_api(
            method="GET", url=f"{self.base_url}/results/{scan_id}/group",
            params=params,
        )
        return response.json()


# ----- Module-level conveniences -----

def get_results(
    scan_id: str,
    filter_: DastResultsFilter = None,
    page: int = None,
    per_page: int = None,
    search: str = None,
    sort_by: List[DastResultsSortBy] = None,
    group: str = None,
) -> DastResultsCollection:
    return DastResultsAPI().get_results(
        scan_id=scan_id, filter_=filter_, page=page, per_page=per_page,
        search=search, sort_by=sort_by, group=group,
    )


def update_results(changelog: DastResultsChangelogInput) -> bool:
    return DastResultsAPI().update_results(changelog=changelog)


def get_result_info(result_id: str, scan_id: str) -> DastResultDetail:
    return DastResultsAPI().get_result_info(result_id=result_id, scan_id=scan_id)


def get_results_count_by_group(scan_id: str, **params) -> dict:
    return DastResultsAPI().get_results_count_by_group(scan_id=scan_id, **params)
