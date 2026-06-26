from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    AiTrProcessStatusResponse,
    AiTriageTriggerRequest,
    AiTriageTriggerResponse,
)


class AiTriageAndRemediationAPI(object):
    """API client for the AI Triage & Remediation REST API.

    These APIs extend the AI Triage & Remediation capability by enabling
    programmatic triggering and status tracking for AI-driven vulnerability
    triage and remediation workflows.

    When a trigger request is submitted, the API returns a processId, which
    can be used to track the status of the asynchronous process.

    AI Triage updates the vulnerability risk state and records a changelog
    with a comment. Currently supported for SAST and SCA scanners only.
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/v1/ai-triage"
        )

    def trigger_ai_triage(
        self, trigger_request: AiTriageTriggerRequest
    ) -> AiTriageTriggerResponse:
        """Trigger an AI Triage of one or more vulnerabilities identified in
        your projects.

        Returns a processId that can be used to track the status of the
        request. Currently supported for SAST and SCA scanners only.

        For SAST vulnerabilities, similarityId and attackVectorId are mutually
        exclusive. Supplying both values in the same request item returns a
        validation error.

        Args:
            trigger_request (AiTriageTriggerRequest): Request body containing a
                list of one or more vulnerabilities to triage. Each
                vulnerability requires a projectId and either a similarityId
                or attackVectorId (for SAST).

        Returns:
            AiTriageTriggerResponse: Response containing the processId
            (unique identifier of the triggered AI Triage process) and
            status (e.g. 'in_progress' or 'rejected').

        Example:
            from CheckmarxPythonSDK.CxOne.dto import (
                AiTriageTriggerRequest,
                AiTriageVulnerability,
            )
            from CheckmarxPythonSDK.CxOne.aiTriageAndRemediationAPI import AiTriageAndRemediationAPI

            request = AiTriageTriggerRequest(
                vulnerabilities=[
                    AiTriageVulnerability(
                        projectId="my-project-id",
                        similarityId="my-similarity-id",
                    )
                ]
            )
            response = AiTriageAndRemediationAPI().trigger_ai_triage(request)
            print(response.processId)
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


    def trigger_ai_remediation(
        self, trigger_request: AiTriageTriggerRequest
    ) -> AiTriageTriggerResponse:
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
            AiTriageTriggerResponse: Response containing the processId
            (unique identifier of the triggered AI Remediation process) and
            status (e.g. 'in_progress' or 'rejected').

        Example:
            from CheckmarxPythonSDK.CxOne.dto import (
                AiTriageTriggerRequest,
                AiTriageVulnerability,
            )
            from CheckmarxPythonSDK.CxOne.aiTriageAndRemediationAPI import AiTriageAndRemediationAPI

            request = AiTriageTriggerRequest(
                vulnerabilities=[
                    AiTriageVulnerability(
                        projectId="my-project-id",
                        similarityId="my-similarity-id",
                    )
                ]
            )
            response = AiTriageAndRemediationAPI().trigger_ai_remediation(request)
            print(response.processId)
        """
        url = f"{self.api_client.configuration.server_base_url}/api/v1/ai-remediation/trigger"
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
        """Retrieve the status of a triggered AI Triage or Remediation process.

        Returns the overall batch status and per-vulnerability status results.
        Use this to poll for completion after triggering a process with
        trigger_ai_triage or trigger_ai_remediation.

        Args:
            process_id (str): Unique identifier of the triggered process,
                returned by trigger_ai_triage or trigger_ai_remediation.

        Returns:
            AiTrProcessStatusResponse: Response containing the overall process
            status (e.g. 'in_progress', 'completed', 'completed_with_errors',
            'failed') and per-vulnerability results.

        Example:
            from CheckmarxPythonSDK.CxOne.aiTriageAndRemediationAPI import AiTriageAndRemediationAPI

            status = AiTriageAndRemediationAPI().retrieve_process_status(
                process_id="my-process-id"
            )
            print(status.status)           # e.g. 'completed'
            for r in status.results:
                print(r.status, r.error)   # per-vulnerability status
        """
        url = f"{self.api_client.configuration.server_base_url}/api/v1/ai-tr/process/{process_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return AiTrProcessStatusResponse.from_dict(response.json())


def trigger_ai_triage(trigger_request: AiTriageTriggerRequest) -> AiTriageTriggerResponse:
    """Trigger an AI Triage of one or more vulnerabilities identified in your
    projects.

    Returns a processId that can be used to track the status of the request.
    Currently supported for SAST and SCA scanners only.

    For SAST vulnerabilities, similarityId and attackVectorId are mutually
    exclusive. Supplying both values in the same request item returns a
    validation error.

    Args:
        trigger_request (AiTriageTriggerRequest): Request body containing a
            list of one or more vulnerabilities to triage. Each vulnerability
            requires a projectId and either a similarityId or attackVectorId
            (for SAST).

    Returns:
        AiTriageTriggerResponse: Response containing the processId (unique
        identifier of the triggered AI Triage process) and status
        (e.g. 'in_progress' or 'rejected').

    Example:
        from CheckmarxPythonSDK.CxOne.dto import (
            AiTriageTriggerRequest,
            AiTriageVulnerability,
        )
        from CheckmarxPythonSDK.CxOne import trigger_ai_triage

        request = AiTriageTriggerRequest(
            vulnerabilities=[
                AiTriageVulnerability(
                    projectId="my-project-id",
                    similarityId="my-similarity-id",
                )
            ]
        )
        response = trigger_ai_triage(request)
        print(response.processId)
    """
    return AiTriageAndRemediationAPI().trigger_ai_triage(trigger_request)


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

    Example:
        from CheckmarxPythonSDK.CxOne.dto import (
            AiTriageTriggerRequest,
            AiTriageVulnerability,
        )
        from CheckmarxPythonSDK.CxOne import trigger_ai_remediation

        request = AiTriageTriggerRequest(
            vulnerabilities=[
                AiTriageVulnerability(
                    projectId="my-project-id",
                    similarityId="my-similarity-id",
                )
            ]
        )
        response = trigger_ai_remediation(request)
        print(response.processId)
    """
    return AiTriageAndRemediationAPI().trigger_ai_remediation(trigger_request)


def retrieve_process_status(process_id: str) -> AiTrProcessStatusResponse:
    """Retrieve the status of a triggered AI Triage or Remediation process.

    Returns the overall batch status and per-vulnerability status results.
    Use this to poll for completion after triggering a process with
    trigger_ai_triage or trigger_ai_remediation.

    Args:
        process_id (str): Unique identifier of the triggered process, returned
            by trigger_ai_triage or trigger_ai_remediation.

    Returns:
        AiTrProcessStatusResponse: Response containing the overall process
        status (e.g. 'in_progress', 'completed', 'completed_with_errors',
        'failed') and per-vulnerability results.

    Example:
        from CheckmarxPythonSDK.CxOne import retrieve_process_status

        status = retrieve_process_status(process_id="my-process-id")
        print(status.status)           # e.g. 'completed'
        for r in status.results:
            print(r.status, r.error)   # per-vulnerability status
    """
    return AiTriageAndRemediationAPI().retrieve_process_status(process_id)
