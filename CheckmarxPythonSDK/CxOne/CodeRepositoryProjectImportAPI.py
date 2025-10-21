from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .utilities import type_check
from .dto import SCMImportInput

api_url = "/api/repos-manager"


class CodeRepositoryProjectImportAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def import_code_repository(self, scm_import_input: SCMImportInput) -> dict:
        """

        Args:
            scm_import_input (SCMImportInput):

        Returns:
            processId
                string
                The unique identifier of this conversion process. You will use this ID with the
                GET conversion/status/{process_id} API to check the status of the conversion.

            message
                string
                A message that includes the url for checking the conversion status.
        """
        type_check(scm_import_input, SCMImportInput)
        relative_url = api_url + "/scm-projects"
        response = self.api_client.post_request(relative_url=relative_url, json=scm_import_input.to_dict())
        item = response.json()
        return {
          "processId": item.get("processId"),
          "message": item.get("message"),
        }

    def retrieve_import_status(self, process_id: str) -> dict:
        """

        Args:
            process_id: The unique identifier of the import process for which you would like to check the status

        Returns:
            example:
            {'currentPhase': 'PROCESSING_REPOSITORIES', 'percentage': 1.0}
            {'currentPhase': 'DONE', 'percentage': 100.0,
                'result': {'status': 'OK', 'totalProjects': 1, 'successfulProjectCount': 1,
                    'successfulProjects': ['happy-cook/JavaVulnerableLab'], 'failedProjects': []}
            }
            :object:
            currentPhase (str): The current phase of the import process. Allowed values:
                PROCESSING_REPOSITORIES
                CONFIGURING_REPOSITORIES
                CREATING_CHECKMARX_ONE_PROJECTS
                DONE
            percentage (int): The percentage of the overall import process that has been completed
            result: Shows the results of the import process Note: This section is returned only when the currentPhase is
                in DONE status.
                status (str): The outcome status of the process. Allowed values: PARTIAL OK FAILURE
                totalProjects (int): The total number of projects that were attempted to create
                successfulProjectCount (int): The number of projects that were successfully created
                successfulProjects (list of str): A list of projects that were successfully created
                failedProjects: A list of projects that failed to be created
                    repoUrl (str):  The URL of the repo
                    error (str): The error that caused the failure

        """
        type_check(process_id, str)
        relative_url = api_url + f"/scm-projects/import-status"
        params = {"process-id": process_id}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        item = response.json()

        response_data = {
          "currentPhase": item.get("currentPhase"),
          "percentage": item.get("percentage"),
        }

        if "result" in item:
            response_data["result"] = item["result"]

        return response_data


def import_code_repository(scm_import_input: SCMImportInput) -> dict:
    return CodeRepositoryProjectImportAPI().import_code_repository(scm_import_input=scm_import_input)


def retrieve_import_status(process_id: str) -> dict:
    return CodeRepositoryProjectImportAPI().retrieve_import_status(process_id=process_id)
