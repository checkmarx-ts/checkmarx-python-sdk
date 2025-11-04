from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration
import time
import json
from CheckmarxPythonSDK.utilities.compat import (OK, CREATED)
from typing import Union
from .dto import (
    CreateReportDTO,
)

headers = {"Content-Type": "application/json; v=1.0"}


class CxReporting(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def retrieve_the_file_of_a_specific_report(self, report_id: int) -> bytes:
        """

        Args:
            report_id (int):

        Returns:
            file content (binary string)
        """
        report_content = None
        relative_url = "/api/reports/{id}".format(id=report_id)
        response = self.api_client.get_request(relative_url=relative_url, headers=headers)
        if response.status_code == OK:
            report_content = response.content
        return report_content

    def create_a_new_report_request(self, report_request: CreateReportDTO) -> Union[int, None]:
        """

        Args:
            report_request (CreateReportDTO):

        Returns:
            report_id (int)
        """
        report_id = None

        if report_request and not isinstance(report_request, CreateReportDTO):
            return report_id
        relative_url = "/api/reports"
        data = json.dumps(report_request.to_dict())
        response = self.api_client.post_request(relative_url=relative_url, data=data, headers=headers)
        if response.status_code == CREATED:
            item = response.json()
            report_id = item.get("reportId")
        return report_id

    def retrieve_the_status_of_a_specific_report(self, report_id: int) -> str:
        """

        Args:
            report_id (int):

        Returns:
            report_status (str)
                NEW
                PROCESSING
                FINISHED
        """
        report_status = None
        relative_url = "/api/reports/{id}/status".format(id=report_id)
        response = self.api_client.get_request(relative_url=relative_url, headers=headers)
        if response.status_code == OK:
            item = response.json()
            report_status = item.get("reportStatus")
        return report_status

    def get_report(self, report_request: CreateReportDTO) -> Union[bytes, None]:
        """

        Args:
            report_request (CreateReportDTO):

        Returns:
            file content (binary string)
        """
        report_id = self.create_a_new_report_request(report_request=report_request)
        if not report_id:
            return None

        report_status = self.retrieve_the_status_of_a_specific_report(report_id=report_id)
        while report_status.upper() != "FINISHED":
            if "FAIL" in report_status.upper():
                print("Report generation failed!")
                return None
            report_status = self.retrieve_the_status_of_a_specific_report(report_id=report_id)
            print("report status: {}".format(report_status))
            time.sleep(2)

        return self.retrieve_the_file_of_a_specific_report(report_id=report_id)


def retrieve_the_file_of_a_specific_report(report_id: int) -> bytes:
    return CxReporting().retrieve_the_file_of_a_specific_report(report_id=report_id)


def create_a_new_report_request(report_request: CreateReportDTO) -> int:
    return CxReporting().create_a_new_report_request(report_request=report_request)


def retrieve_the_status_of_a_specific_report(report_id: int) -> str:
    return CxReporting().retrieve_the_status_of_a_specific_report(report_id=report_id)


def get_report(report_request: CreateReportDTO) -> Union[bytes, None]:
    return CxReporting().get_report(report_request=report_request)
