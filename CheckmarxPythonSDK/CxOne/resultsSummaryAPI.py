from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import (
    ResultsSummary,
)

api_url = "/api/scan-summary"


class ResultsSummaryAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_summary_for_many_scans(
            self, scan_ids: List[str], include_severity_status: bool = True, include_queries: bool = False,
            include_files: bool = False, apply_predicates: bool = True, language: str = None
    ) -> dict:
        """

        Args:
            scan_ids (list of str): Scan IDs to find. Each scan id will have his own object.
            include_severity_status (bool): if true returns the severityStatus field, otherwise will omit the field.
                                Default value : true
            include_queries (bool): if true returns the queries field, otherwise will omit the field.
                                Default value : false
            include_files (bool): if true returns the source code file and sink code file fields, otherwise will omit
                                the fields.
                                Default value : false
            apply_predicates (bool): if true will apply changes from predicates, otherwise will return the raw results
                                summary.
                                Default value : true
            language (str): get scan summary for specific source code language.

        Returns:
            dict
        """
        type_check(scan_ids, (list, tuple))
        type_check(include_severity_status, bool)
        type_check(include_queries, bool)
        type_check(include_files, bool)
        type_check(apply_predicates, bool)
        type_check(language, str)

        list_member_type_check(scan_ids, str)

        relative_url = api_url
        params = {
            "scan-ids": scan_ids, "include-severity-status": include_severity_status,
            "include-queries": include_queries, "include-files": include_files,
            "apply-predicates": apply_predicates, "language": language,
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        response = response.json()
        return {
            "scansSummaries": [
                ResultsSummary(
                    scan_id=summary.get("scanId"),
                    sast_counters=summary.get("sastCounters"),
                    kics_counters=summary.get("kicsCounters"),
                    sca_counters=summary.get("scaCounters"),
                    sca_packages_counters=summary.get('scaPackagesCounters'),
                    sca_containers_counters=summary.get('scaContainersCounters'),
                    api_sec_counters=summary.get('apiSecCounters')
                ) for summary in response.get("scansSummaries") or []
            ],
            "totalCount": response.get("totalCount")
        }


def get_summary_for_many_scans(
        scan_ids: List[str], include_severity_status: bool = True, include_queries: bool = False,
        include_files: bool = False, apply_predicates: bool = True, language: str = None
) -> dict:
    return ResultsSummaryAPI().get_summary_for_many_scans(
        scan_ids=scan_ids, include_severity_status=include_severity_status, include_queries=include_queries,
        include_files=include_files, apply_predicates=apply_predicates, language=language
    )
