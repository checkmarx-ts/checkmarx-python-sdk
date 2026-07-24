from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    AiRemediationRequest,
    AiRemediationResponse,
    AiRemediationDetails,
)


class AiRemediationAPI(object):
    """API client for the AI Remediation REST API.

    Submits requests to generate AI-powered remediation for vulnerabilities
    within a scan and retrieves remediation details. AI Remediation first runs
    AI Triage and then, when applicable, opens a pull request with the
    suggested remediation. For manual projects, the remediation workflow
    updates the RO table without opening a pull request. Currently supported
    for SAST and SCA scanners only.
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/remediation"
        )

    def trigger_ai_remediation(
        self, remediation_request: AiRemediationRequest
    ) -> AiRemediationResponse:
        """Submit a request to generate AI-powered remediation for one or more
        vulnerabilities within a scan.

        The request is processed asynchronously. A successful request returns
        202 Accepted. Use retrieve_ai_remediation_details to poll for results.

        Args:
            remediation_request (AiRemediationRequest): Request body containing
                the scan ID and one or more scanner buckets (scannerType +
                resultIDs). Result IDs are obtained from the alternateId field
                returned by GET /api/results. URL-encoding the IDs is highly
                recommended. At least one bucket is required.

        Returns:
            AiRemediationResponse: Response containing status ('accepted'),
            published flag, existingState, and remediationJobId.
        """
        url = f"{self.base_url}/remediate"
        response = self.api_client.call_api(
            method="POST",
            url=url,
            headers={"Accept": "application/json"},
            json=remediation_request.to_dict(),
        )
        return AiRemediationResponse.from_dict(response.json())

    def retrieve_ai_remediation_details(
        self, scan_id: str, result_id: str
    ) -> AiRemediationDetails:
        """Retrieve AI Remediation details for a specific vulnerability within
        a scan.

        If remediation is still in progress or has failed, the response
        contains the current job status. Otherwise, the completed remediation
        details are returned.

        Args:
            scan_id (str): Unique identifier of the scan.
            result_id (str): Use the alternateId returned by GET /api/results.
                URL-encoding is highly recommended.

        Returns:
            AiRemediationDetails: Scan ID and per-result remediation details
            including auto-PR status, code diffs, analysis, and generated
            tests.
        """
        url = f"{self.base_url}/remediation-details/{scan_id}/{result_id}"
        response = self.api_client.call_api(
            method="GET",
            url=url,
            headers={"Accept": "application/json"},
        )
        return AiRemediationDetails.from_dict(response.json())


def trigger_ai_remediation(
    remediation_request: AiRemediationRequest,
) -> AiRemediationResponse:
    """Submit a request to generate AI-powered remediation for one or more
    vulnerabilities within a scan.

    The request is processed asynchronously. A successful request returns
    202 Accepted. Use retrieve_ai_remediation_details to poll for results.

    Args:
        remediation_request (AiRemediationRequest): Request body containing the
            scan ID and one or more scanner buckets (scannerType + resultIDs).
            Result IDs are obtained from the alternateId field returned by
            GET /api/results. URL-encoding the IDs is highly recommended. At
            least one bucket is required.

    Returns:
        AiRemediationResponse: Response containing status ('accepted'),
        published flag, existingState, and remediationJobId.
    """
    return AiRemediationAPI().trigger_ai_remediation(remediation_request)


def retrieve_ai_remediation_details(scan_id: str, result_id: str) -> AiRemediationDetails:
    """Retrieve AI Remediation details for a specific vulnerability within a
    scan.

    If remediation is still in progress or has failed, the response contains
    the current job status. Otherwise, the completed remediation details are
    returned.

    Args:
        scan_id (str): Unique identifier of the scan.
        result_id (str): Use the alternateId returned by GET /api/results.
            URL-encoding is highly recommended.

    Returns:
        AiRemediationDetails: Scan ID and per-result remediation details
        including auto-PR status, code diffs, analysis, and generated tests.
    """
    return AiRemediationAPI().retrieve_ai_remediation_details(scan_id, result_id)
