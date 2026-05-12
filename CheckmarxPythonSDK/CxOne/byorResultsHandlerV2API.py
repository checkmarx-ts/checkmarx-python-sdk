# encoding: utf-8
from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .dto import (
    ImportRequest,
    ImportResults,
    ByorJob,
    ByorJobPatchRequest,
)


class ByorResultsHandlerV2API(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/v2/byor"
        )

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

    def get_job_by_id(self, job_id: str) -> ByorJob:
        """
        Args:
            job_id (str):

        Returns:
            ByorJob
        """
        url = f"{self.base_url}/jobs/{job_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return ByorJob.from_dict(response.json())

    def patch_job_by_id(
        self,
        job_id: str,
        patch_request: ByorJobPatchRequest = ByorJobPatchRequest(status="Canceled"),
    ) -> bool:
        """
        Args:
            job_id (str):
            patch_request (ByorJobPatchRequest):

        Returns:
            bool
        """
        url = f"{self.base_url}/jobs/{job_id}"
        response = self.api_client.call_api(
            method="PATCH", url=url, json=asdict(patch_request)
        )
        return response.status_code == NO_CONTENT


def create_byor_import(import_request) -> ImportResults:
    return ByorResultsHandlerV2API().create_byor_import(import_request)


def get_job_by_id(job_id: str) -> ByorJob:
    return ByorResultsHandlerV2API().get_job_by_id(job_id=job_id)


def patch_job_by_id(job_id: str, patch_request: ByorJobPatchRequest) -> bool:
    return ByorResultsHandlerV2API().patch_job_by_id(
        job_id=job_id, patch_request=patch_request
    )
