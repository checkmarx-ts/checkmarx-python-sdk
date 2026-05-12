from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .dto import (
    ImportRequest,
    ImportResults,
    TriageRequest,
    TriageResponse,
)


class ByorResultsHandlerAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = f"{self.api_client.configuration.server_base_url}/api/v1/byor"

    def create_byor_import(self, import_request: ImportRequest) -> ImportResults:
        """
        Args:
            import_request (ImportRequest):

        Returns:
            ImportResults
        """
        url = f"{self.base_url}/imports"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(import_request)
        )
        return ImportResults.from_dict(response.json())

    def save_triage(self, triage_request: TriageRequest) -> bool:
        """
        Args:
            triage_request (TriageRequest):

        Returns:
            bool
        """
        url = f"{self.base_url}/triage"
        response = self.api_client.call_api(
            method="POST", url=url, json={k: v for k, v in asdict(triage_request).items() if v is not None}
        )
        return response.status_code == NO_CONTENT

    def get_triage(self, result_id: str, project_id: str) -> TriageResponse:
        """
        Args:
            result_id (str): Returning triage specified by encoded result ID.
                (Exact match, case-sensitive)
            project_id (str): Returning triage specified by project ID.
                (Exact match, case-sensitive)

        Returns:
            TriageResponse
        """
        url = f"{self.base_url}/triage"
        params = {"result-id": result_id, "project-id": project_id}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return TriageResponse.from_dict(response.json())


def create_byor_import(import_request) -> ImportResults:
    return ByorResultsHandlerAPI().create_byor_import(import_request)


def save_triage(triage_request: TriageRequest) -> bool:
    return ByorResultsHandlerAPI().save_triage(triage_request=triage_request)


def get_triage(result_id: str, project_id: str) -> TriageResponse:
    return ByorResultsHandlerAPI().get_triage(
        result_id=result_id, project_id=project_id
    )
