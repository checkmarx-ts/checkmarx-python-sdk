from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .utilities import type_check
from .dto import (
    ImportRequest,
    ImportResults, construct_import_results,
    TriageRequest,
    TriageResponse, construct_triage_response,
)

api_url = "/api/v1/byor"


class ByorResultsHandlerAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def create_byor_import(self, import_request: ImportRequest) -> ImportResults:
        """

        Args:
            import_request (ImportRequest):

        Returns:
            ImportResults
        """
        type_check(import_request, ImportRequest)
        relative_url = api_url + "/imports"
        response = self.api_client.post_request(relative_url=relative_url, json=import_request.to_dict())
        item = response.json()
        return construct_import_results(item)

    def save_triage(self, triage_request: TriageRequest) -> bool:
        """

        Args:
            triage_request (TriageRequest):

        Returns:
            bool
        """
        relative_url = api_url + "/triage"
        response = self.api_client.post_request(relative_url=relative_url, json=triage_request.to_dict())
        return response.status_code == NO_CONTENT

    def get_triage(self, result_id: str, project_id: str) -> TriageResponse:
        """

        Args:
            result_id (str): Returning triage specified by encoded result ID. (Exact match, case-sensitive)
            project_id (str): Returning triage specified by project ID. (Exact match, case-sensitive)

        Returns:
            TriageResponse
        """
        relative_url = api_url + "/triage"
        params = {"result-id": result_id, "project-id": project_id}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        item = response.json()
        return construct_triage_response(item)


def create_byor_import(import_request) -> ImportResults:
    return ByorResultsHandlerAPI().create_byor_import(import_request)


def save_triage(triage_request: TriageRequest) -> bool:
    return ByorResultsHandlerAPI().save_triage(triage_request=triage_request)


def get_triage(result_id: str, project_id: str) -> TriageResponse:
    return ByorResultsHandlerAPI().get_triage(result_id=result_id, project_id=project_id)
