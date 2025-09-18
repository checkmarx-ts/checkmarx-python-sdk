from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import construct_result

api_url = "/api/results"


class ScannersResultsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_all_scanners_results_by_scan_id(
            self, scan_id: str, severity: List[str] = None, state: List[str] = None, status: List[str] = None,
            offset: int = 0, limit: int = 20, sort: List[str] = ("+status", "+severity")
    ) -> dict:
        """

        Args:
            scan_id (str): filter by scan id
            severity (list of str): filter by severity. OR operator between the items
                                    Available values : HIGH, MEDIUM, LOW, INFO
            state (list of str): filter by state. OR operator between the items.
                            Available values : TO_VERIFY, NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT
            status (list of str): filter by status. OR operator between the items.
                            Available values : NEW, RECURRENT, FIXED
            offset (int): The number of items to skip before starting to collect the result set.
                            Default value : 0
            limit (int): The number of items to return.
                            Default value : 20
            sort (list of str): sorting ORDERED array. each string pattern "[-+]field". - mean ASC, + mean DESC.
                            Available values : -severity, +severity, -status, +status, -state, +state, -type, +type,
                                        -firstfoundat, +firstfoundat, -foundat, +foundat, -firstscanid, +firstscanid
                            Default value : List [ "+status", "+severity" ]

        Returns:
            dict
        """
        type_check(scan_id, str)
        type_check(severity, (list, tuple))
        type_check(state, (list, tuple))
        type_check(status, (list, tuple))
        type_check(offset, int)
        type_check(limit, int)
        type_check(sort, (list, tuple))

        list_member_type_check(severity, str)
        list_member_type_check(state, str)
        list_member_type_check(status, str)
        list_member_type_check(sort, str)

        relative_url = api_url
        params = {
            "scan-id": scan_id, "severity": severity, "state": state, "status": status, "offset": offset,
            "limit": limit, "sort": ",".join(sort) if sort else None
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        response = response.json()
        return {
            "results": [
                construct_result(result) for result in response.get("results") or []
            ],
            "totalCount": response.get("totalCount"),
        }


def get_all_scanners_results_by_scan_id(
        scan_id: str, severity: List[str] = None, state: List[str] = None, status: List[str] = None,
        offset: int = 0, limit: int = 20, sort: List[str] = ("+status", "+severity")
) -> dict:
    return ScannersResultsAPI().get_all_scanners_results_by_scan_id(
        scan_id=scan_id, severity=severity, state=state, status=status, offset=offset, limit=limit, sort=sort
    )
