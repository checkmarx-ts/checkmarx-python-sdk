from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import KicsResultCollection


class KicsResultsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/kics-results"
        )

    def get_kics_results_by_scan_id(
        self,
        scan_id: str,
        severity: List[str] = None,
        status: List[str] = None,
        source_file: str = None,
        apply_predicates: bool = True,
        offset: int = 0,
        limit: int = 20,
        sort: List[str] = ("+status", "+severity"),
    ) -> KicsResultCollection:
        """
        Args:
            scan_id (str): filter by scan id
            severity (List[str]): filter by severity (OR). Available values:
                HIGH, MEDIUM, LOW, INFO
            status (List[str]): filter by status (OR). Available values:
                NEW, RECURRENT, FIXED
            source_file (str): filter by source file name
            apply_predicates (bool): if true apply predicate changes.
                Default value: true
            offset (int): items to skip before collecting results.
                Default value: 0
            limit (int): number of items to return. Default value: 20
            sort (List[str]): sort criteria array, e.g. ["+status", "-severity"].
                Available values: -severity, +severity, -status, +status,
                -firstfoundat, +firstfoundat, -foundat, +foundat,
                firstscanid, +firstscanid. Default: ["+status", "+severity"]

        Returns:
            KicsResultCollection
        """
        params = {
            "scan-id": scan_id,
            "severity": severity,
            "status": status,
            "source-file": source_file,
            "apply-predicates": apply_predicates,
            "offset": offset,
            "limit": limit,
            "sort": ",".join(sort) if sort else None,
        }
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        return KicsResultCollection.from_dict(response.json())


def get_kics_results_by_scan_id(
    scan_id: str,
    severity: List[str] = None,
    status: List[str] = None,
    source_file: str = None,
    apply_predicates: bool = True,
    offset: int = 0,
    limit: int = 20,
    sort: List[str] = ("+status", "+severity"),
) -> KicsResultCollection:
    return KicsResultsAPI().get_kics_results_by_scan_id(
        scan_id=scan_id,
        severity=severity,
        status=status,
        source_file=source_file,
        apply_predicates=apply_predicates,
        offset=offset,
        limit=limit,
        sort=sort,
    )
