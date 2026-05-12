from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import ResultsSummary


class ResultsSummaryAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            "/api/scan-summary"
        )

    def get_summary_for_many_scans(
        self,
        scan_ids: List[str],
        include_severity_status: bool = True,
        include_queries: bool = False,
        include_files: bool = False,
        apply_predicates: bool = True,
        language: str = None,
    ) -> dict:
        """
        Args:
            scan_ids (List[str]): Scan IDs to find. Each scan id will
                have its own object.
            include_severity_status (bool): If true, returns the
                severityStatus field. Default: true
            include_queries (bool): If true, returns the queries field.
                Default: false
            include_files (bool): If true, returns the source code file
                and sink code file fields. Default: false
            apply_predicates (bool): If true, applies changes from
                predicates. Default: true
            language (str): Get scan summary for specific source code
                language.

        Returns:
            dict
        """
        params = {
            "scan-ids": scan_ids,
            "include-severity-status": include_severity_status,
            "include-queries": include_queries,
            "include-files": include_files,
            "apply-predicates": apply_predicates,
            "language": language,
        }
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        data = response.json()
        return {
            "scansSummaries": [
                ResultsSummary.from_dict(summary)
                for summary in (data.get("scansSummaries") or [])
            ],
            "totalCount": data.get("totalCount"),
        }


def get_summary_for_many_scans(
    scan_ids: List[str],
    include_severity_status: bool = True,
    include_queries: bool = False,
    include_files: bool = False,
    apply_predicates: bool = True,
    language: str = None,
) -> dict:
    return ResultsSummaryAPI().get_summary_for_many_scans(
        scan_ids=scan_ids,
        include_severity_status=include_severity_status,
        include_queries=include_queries,
        include_files=include_files,
        apply_predicates=apply_predicates,
        language=language,
    )
