from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import SastComparisonStatus


class SastResultsCompareAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/scans-compare/sast"
        )

    def get_compare_status(
        self,
        scan_id: str,
        base_scan_id: str,
        evaluation_status: bool = None,
        correlation_id: str = None,
    ) -> SastComparisonStatus:
        """GET /api/scans-compare/sast/status -- compares two SAST
        scans of a single project, returning aggregate counts of
        vulnerabilities by severity and status.

        Args:
            scan_id (str): Required. Scan ID of the newer scan.
            base_scan_id (str): Required. Scan ID of the older
                (baseline) scan.
            evaluation_status (bool): If true, enables reclassification
                of FIXED results as NOT_EVALUATED.
            correlation_id (str): Optional UUID, for internal
                Checkmarx use.

        Returns:
            SastComparisonStatus
        """
        url = f"{self.base_url}/status"
        params = {
            "scan-id": scan_id,
            "base-scan-id": base_scan_id,
            "evaluation-status": evaluation_status,
        }
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers,
        )
        return SastComparisonStatus.from_dict(response.json())


# ---- Module-level convenience function ----

def get_compare_status(
    scan_id: str,
    base_scan_id: str,
    evaluation_status: bool = None,
    correlation_id: str = None,
) -> SastComparisonStatus:
    return SastResultsCompareAPI().get_compare_status(
        scan_id=scan_id,
        base_scan_id=base_scan_id,
        evaluation_status=evaluation_status,
        correlation_id=correlation_id,
    )
