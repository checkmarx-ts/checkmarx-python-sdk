from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    AiTrProcessStatusResponse,
    AiTriageTriggerRequest,
    AiTriageTriggerResponse,
)


class AiRemediationAPI(object):
    """API client for the AI Remediation REST API.

    Enables programmatic triggering and status tracking for AI-driven
    vulnerability remediation workflows. AI Remediation first runs AI Triage
    and then, when applicable, opens a pull request with the suggested
    remediation. For manual projects, the remediation workflow updates the RO
    table without opening a pull request.

    When a trigger request is submitted, the API returns a processId that can
    be used to track the asynchronous process. Currently supported for SAST
    and SCA scanners only.
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/v1/ai-remediation"
        )

    def trigger_ai_remediation(
        self, trigger_request: AiTriageTriggerRequest
    ) -> AiTriageTriggerResponse:
        """Trigger an AI Remediation of one or more vulnerabilities identified
        in your projects.

        AI Remediation first runs AI Triage and then, when applicable, opens a
        pull request with the suggested remediation. For manual projects, the
        remediation workflow updates the RO table without opening a pull
        request.

        Returns a processId that can be used to track the status of the
        request. Currently supported for SAST and SCA scanners only.

        For SAST vulnerabilities, similarityId and attackVectorId are mutually
        exclusive. Supplying both values in the same request item returns a
        validation error.

        Args:
            trigger_request (AiTriageTriggerRequest): Request body containing a
                list of one or more vulnerabilities to remediate. Each
                vulnerability requires a projectId and either a similarityId
                or attackVectorId (for SAST).

        Returns:
            AiTriageTriggerResponse: Response containing the processId
            (unique identifier of the triggered AI Remediation process) and
            status (e.g. 'in_progress' or 'rejected').
        """
        url = f"{self.base_url}/trigger"
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json={
                "vulnerabilities": [
                    v.to_dict() for v in trigger_request.vulnerabilities
                ]
            },
        )
        return AiTriageTriggerResponse.from_dict(response.json())

    def retrieve_process_status(
        self, process_id: str
    ) -> AiTrProcessStatusResponse:
        """Retrieve the status of a triggered AI Remediation process.

        Returns the overall batch status and per-vulnerability status results.
        Use this to poll for completion after triggering a process with
        trigger_ai_remediation.

        Args:
            process_id (str): Unique identifier of the triggered process,
                returned by trigger_ai_remediation.

        Returns:
            AiTrProcessStatusResponse: Response containing the overall process
            status (e.g. 'in_progress', 'completed', 'completed_with_errors',
            'failed') and per-vulnerability results.
        """
        url = f"{self.api_client.configuration.server_base_url}/api/v1/ai-tr/process/{process_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return AiTrProcessStatusResponse.from_dict(response.json())


def trigger_ai_remediation(trigger_request: AiTriageTriggerRequest) -> AiTriageTriggerResponse:
    """Trigger an AI Remediation of one or more vulnerabilities identified in
    your projects.

    AI Remediation first runs AI Triage and then, when applicable, opens a
    pull request with the suggested remediation. For manual projects, the
    remediation workflow updates the RO table without opening a pull request.

    Returns a processId that can be used to track the status of the request.
    Currently supported for SAST and SCA scanners only.

    For SAST vulnerabilities, similarityId and attackVectorId are mutually
    exclusive. Supplying both values in the same request item returns a
    validation error.

    Args:
        trigger_request (AiTriageTriggerRequest): Request body containing a
            list of one or more vulnerabilities to remediate. Each
            vulnerability requires a projectId and either a similarityId
            or attackVectorId (for SAST).

    Returns:
        AiTriageTriggerResponse: Response containing the processId (unique
        identifier of the triggered AI Remediation process) and status
        (e.g. 'in_progress' or 'rejected').
    """
    return AiRemediationAPI().trigger_ai_remediation(trigger_request)


def retrieve_process_status(process_id: str) -> AiTrProcessStatusResponse:
    """Retrieve the status of a triggered AI Remediation process.

    Returns the overall batch status and per-vulnerability status results.
    Use this to poll for completion after triggering a process with
    trigger_ai_remediation.

    Args:
        process_id (str): Unique identifier of the triggered process, returned
            by trigger_ai_remediation.

    Returns:
        AiTrProcessStatusResponse: Response containing the overall process
        status (e.g. 'in_progress', 'completed', 'completed_with_errors',
        'failed') and per-vulnerability results.
    """
    return AiRemediationAPI().retrieve_process_status(process_id)
