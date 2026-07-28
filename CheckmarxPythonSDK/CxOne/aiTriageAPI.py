import json

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    AiTriageRequest,
    AiTriageResponse,
    AiTriageResult,
)


class AiTriageAPI(object):
    """API client for the AI Triage REST API.

    Submits requests to triage vulnerabilities within a scan and retrieves
    triage results. AI Triage updates the vulnerability risk state and records
    a changelog with a comment. Currently supported for SAST and SCA scanners.
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/ai-triage"
        )

    def trigger_ai_triage(
        self, triage_request: AiTriageRequest
    ) -> AiTriageResponse:
        """Submit a request to triage vulnerabilities within a scan.

        The request is processed asynchronously. A successful request returns
        202 Accepted. Use retrieve_ai_triage_results to poll for results.

        Args:
            triage_request (AiTriageRequest): Request body containing the scan
                ID and one or more scanner buckets (scannerType + resultIDs).
                Result IDs are obtained from the alternateId field returned by
                GET /api/results. URL-encoding the IDs is highly recommended.

        Returns:
            AiTriageResponse: Response containing scanID, status ('accepted'),
            triageID, published flag, and existingTriageState.
        """
        url = f"{self.base_url}/triage"
        response = self.api_client.call_api(
            method="POST",
            url=url,
            headers={"Accept": "application/json"},
            json=triage_request.to_dict(),
        )
        return AiTriageResponse.from_dict(response.json())

    def get_ai_triage_status(
        self, engine: str, group_id: int, project_id: str
    ) -> AiTriageResult:
        """Poll the SSE gateway for real-time AI Triage status updates.

        Connects to the Server-Sent Events endpoint and blocks until the
        stream closes, then returns the last triage status event received.
        Heartbeat frames (`:heartbeat`) are ignored.

        Args:
            engine (str): Scanner engine type, e.g. "sast".
            group_id (int): Vulnerability group identifier (the similarityId
                of the SAST result).
            project_id (str): Unique identifier of the project.

        Returns:
            AiTriageResult: The last triage status event from the SSE stream,
            or an empty AiTriageResult if the stream contained only heartbeats.
        """
        url = (
            f"{self.api_client.configuration.server_base_url}"
            "/api/ssegateway/triage-status"
        )
        params = {
            "engine": engine,
            "groupId": group_id,
            "projectId": project_id,
        }
        response = self.api_client.call_api(
            method="GET",
            url=url,
            params=params,
            headers={"Accept": "text/event-stream"},
        )
        last_event = {}
        for line in response.text.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                payload = line[len("data:"):].strip()
                try:
                    last_event = json.loads(payload)
                except json.JSONDecodeError:
                    pass
        return AiTriageResult.from_dict(last_event)

    def retrieve_ai_triage_results(
        self, project_id: str, group_id: str
    ) -> AiTriageResult:
        """Retrieve AI Triage results for a vulnerability group within a project.

        Returns the full triage analysis if triage has completed, or the
        current job status if still in progress. If the triage operation
        failed, returns a failed job status.

        The recommended way to obtain group_id is to call GET /api/risks for
        the specified project and use the groupId field of the corresponding
        risk object. If group_id contains reserved URL characters (e.g. #),
        URL-encode the value before passing it (replace # with %23).

        Args:
            project_id (str): Unique identifier of the project.
            group_id (str): Identifier of the vulnerability group. URL-encode
                if the value contains reserved characters.

        Returns:
            AiTriageResult: Triage verdict, summary, confidence score,
            reachability, exploitability, and supporting analysis details.
        """
        url = f"{self.base_url}/triage/{project_id}/{group_id}"
        response = self.api_client.call_api(
            method="GET",
            url=url,
            headers={"Accept": "application/json"},
        )
        return AiTriageResult.from_dict(response.json())


def get_ai_triage_status(
    engine: str, group_id: int, project_id: str
) -> AiTriageResult:
    """Poll the SSE gateway for real-time AI Triage status updates.

    Connects to the Server-Sent Events endpoint and blocks until the stream
    closes, then returns the last triage status event received. Heartbeat
    frames (`:heartbeat`) are ignored.

    Args:
        engine (str): Scanner engine type, e.g. "sast".
        group_id (int): Vulnerability group identifier (the similarityId of
            the SAST result).
        project_id (str): Unique identifier of the project.

    Returns:
        AiTriageResult: The last triage status event from the SSE stream, or
        an empty AiTriageResult if the stream contained only heartbeats.
    """
    return AiTriageAPI().get_ai_triage_status(engine, group_id, project_id)


def trigger_ai_triage(triage_request: AiTriageRequest) -> AiTriageResponse:
    """Submit a request to triage vulnerabilities within a scan.

    The request is processed asynchronously. A successful request returns
    202 Accepted. Use retrieve_ai_triage_results to poll for results.

    Args:
        triage_request (AiTriageRequest): Request body containing the scan ID
            and one or more scanner buckets (scannerType + resultIDs). Result
            IDs are obtained from the alternateId field returned by
            GET /api/results. URL-encoding the IDs is highly recommended.

    Returns:
        AiTriageResponse: Response containing scanID, status ('accepted'),
        triageID, published flag, and existingTriageState.
    """
    return AiTriageAPI().trigger_ai_triage(triage_request)


def retrieve_ai_triage_results(project_id: str, group_id: str) -> AiTriageResult:
    """Retrieve AI Triage results for a vulnerability group within a project.

    Returns the full triage analysis if triage has completed, or the current
    job status if still in progress. If the triage operation failed, returns
    a failed job status.

    The recommended way to obtain group_id is to call GET /api/risks for the
    specified project and use the groupId field of the corresponding risk
    object. If group_id contains reserved URL characters (e.g. #), URL-encode
    the value before passing it (replace # with %23).

    Args:
        project_id (str): Unique identifier of the project.
        group_id (str): Identifier of the vulnerability group. URL-encode if
            the value contains reserved characters.

    Returns:
        AiTriageResult: Triage verdict, summary, confidence score,
        reachability, exploitability, and supporting analysis details.
    """
    return AiTriageAPI().retrieve_ai_triage_results(project_id, group_id)
