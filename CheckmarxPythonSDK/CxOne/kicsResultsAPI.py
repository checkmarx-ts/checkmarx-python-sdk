from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import (
    KicsResultCollection, construct_kics_result_collection
)

api_url = "/api/kics-results"


class KicsResultsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_kics_results_by_scan_id(
            self, scan_id: str, severity: List[str] = None, status: List[str] = None, source_file: str = None,
            apply_predicates: bool = True, offset: int = 0, limit: int = 20, sort: List[str] = ("+status", "+severity")
    ) -> KicsResultCollection:
        """

        Args:
            scan_id (str): filter by scan id
            severity (list of str): filter by severity. OR operator between the items.
                                Available values : HIGH, MEDIUM, LOW, INFO
            status (list of str): filter by status. OR operator between the items.
                                Available values : NEW, RECURRENT, FIXED
            source_file (str): filter by source file name.
            apply_predicates (bool): if true will apply changes from predicates, otherwise will return the raw result.
                        Default value : true
            offset (int): The number of items to skip before starting to collect the result set.
                        Default value : 0
            limit (int): The number of items to return.
                        Default value : 20
            sort (list of str): sorting ORDERED array. each string pattern "[-+]field". - mean ASC, + mean DESC.
                        Available values : -severity, +severity, -status, +status, -firstfoundat, +firstfoundat,
                         -foundat, +foundat, firstscanid, +firstscanid
                        Default value : List [ "+status", "+severity" ]
        Returns:
            KicsResultCollection
        """
        type_check(scan_id, str)
        type_check(severity, (list, tuple))
        type_check(status, (list, tuple))
        type_check(source_file, str)
        type_check(apply_predicates, bool)
        type_check(sort, (list, tuple))
        list_member_type_check(severity, str)
        list_member_type_check(status, str)
        list_member_type_check(sort, str)
        relative_url = api_url
        params = {"scan-id": scan_id, "severity": severity, "status": "status", "offset": offset, "limit": limit,
                  "sort": ",".join(sort) if sort else None}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        item = response.json()
        return construct_kics_result_collection(item)


def get_kics_results_by_scan_id(
        scan_id: str, severity: List[str] = None, status: List[str] = None, source_file: str = None,
        apply_predicates: bool = True, offset: int = 0, limit: int = 20, sort: List[str] = ("+status", "+severity")
) -> KicsResultCollection:
    """

    Args:
        scan_id (str): filter by scan id
        severity (List[str]): filter by severity. OR operator between the items. Available values : HIGH, MEDIUM, LOW,
                             INFO
        status (List[str]):  filter by status. OR operator between the items. Available values : NEW, RECURRENT, FIXED
        source_file (str): filter by source file name.
        apply_predicates (bool):  if true will apply changes from predicates, otherwise will return the raw result.
        offset (int): The number of items to skip before starting to collect the result set. Default value : 0
        limit (int):  The number of items to return. Default value : 20
        sort (List[str]):  sorting ORDERED array. each string pattern "[-+]field". - mean ASC, + mean DESC.
                    Available values : -severity, +severity, -status, +status, -firstfoundat, +firstfoundat, -foundat,
                    +foundat, firstscanid, +firstscanid Default value : List [ "+status", "+severity" ]
    Returns:
        KicsResultCollection
    """
    return KicsResultsAPI().get_kics_results_by_scan_id(
        scan_id=scan_id, severity=severity, status=status, source_file=source_file, apply_predicates=apply_predicates,
        offset=offset, limit=limit, sort=sort
    )
