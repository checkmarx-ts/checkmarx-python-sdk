from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import Result


class ScannersResultsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/results"
        )

    def get_all_scanners_results_by_scan_id(
        self,
        scan_id: str,
        severity: List[str] = None,
        state: List[str] = None,
        status: List[str] = None,
        offset: int = 0,
        limit: int = 20,
        sort: List[str] = ("+status", "+severity"),
    ) -> dict:
        """
        Args:
            scan_id (str): Filter by scan id.
            severity (list of str): Filter by severity (OR between items).
                Values: HIGH, MEDIUM, LOW, INFO
            state (list of str): Filter by state (OR between items).
                Values: TO_VERIFY, NOT_EXPLOITABLE,
                PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT
            status (list of str): Filter by status (OR between items).
                Values: NEW, RECURRENT, FIXED
            offset (int): Items to skip. Default: 0.
            limit (int): Items to return. Default: 20.
            sort (list of str): Ordered sort array, each "[-+]field".
                Values: severity, status, state, type, firstfoundat,
                foundat, firstscanid

        Returns:
            dict
        """
        params = {
            "scan-id": scan_id,
            "severity": severity,
            "state": state,
            "status": status,
            "offset": offset,
            "limit": limit,
            "sort": ",".join(sort) if sort else None,
        }
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        resp = response.json()
        return {
            "results": [
                Result.from_dict(r) for r in (resp.get("results") or [])
            ],
            "totalCount": resp.get("totalCount"),
        }


def get_all_scanners_results_by_scan_id(
    scan_id: str,
    severity: List[str] = None,
    state: List[str] = None,
    status: List[str] = None,
    offset: int = 0,
    limit: int = 20,
    sort: List[str] = ("+status", "+severity"),
) -> dict:
    return ScannersResultsAPI().get_all_scanners_results_by_scan_id(
        scan_id=scan_id,
        severity=severity,
        state=state,
        status=status,
        offset=offset,
        limit=limit,
        sort=sort,
    )
