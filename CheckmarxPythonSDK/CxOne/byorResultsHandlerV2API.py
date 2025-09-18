# encoding: utf-8
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .utilities import type_check
from .dto import (
    ImportRequest,
    ImportResults, construct_import_results,
    ByorJob, construct_byor_job,
    ByorJobPatchRequest,
)

api_url = "/api/v2/byor"


class ByorResultsHandlerV2API(object):

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

    def get_job_by_id(self, job_id: str) -> ByorJob:
        """

        Args:
            job_id (str):

        Returns:
            ByorJob
        """
        relative_url = api_url + f"/jobs/{job_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_byor_job(item)

    def patch_job_by_id(
            self, job_id: str, patch_request: ByorJobPatchRequest = ByorJobPatchRequest(status="Canceled ")
    ) -> bool:
        """

        Args:
            job_id (str):
            patch_request (ByorJobPatchRequest ):

        Returns:
            bool
        """
        relative_url = api_url + f"/jobs/{job_id}"
        response = self.api_client.patch_request(relative_url=relative_url, json=patch_request.to_dict())
        return response.status_code == NO_CONTENT


def create_byor_import(import_request) -> ImportResults:
    return ByorResultsHandlerV2API().create_byor_import(import_request)


def get_job_by_id(job_id: str) -> ByorJob:
    return ByorResultsHandlerV2API().get_job_by_id(job_id=job_id)


def patch_job_by_id(job_id: str, patch_request: ByorJobPatchRequest) -> bool:
    return ByorResultsHandlerV2API().patch_job_by_id(job_id=job_id, patch_request=patch_request)
