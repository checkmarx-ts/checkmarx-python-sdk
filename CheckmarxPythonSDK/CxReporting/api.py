from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration
import time
import json
from CheckmarxPythonSDK.utilities.compat import OK, CREATED
from typing import Union
import logging
logger = logging.getLogger(__name__)
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
        self.base_url = api_client.configuration.server_base_url.rstrip("/")

    def retrieve_the_file_of_a_specific_report(
        self, report_id: int, timeout: float = None
    ) -> bytes:
        """

        Args:
            report_id (int):
            timeout (float): per-call timeout in seconds; defaults to the
                configured timeout. Raise it for very large reports.

        Returns:
            file content (binary string)
        """
        report_content = None
        url = f"{self.base_url}/api/reports/{report_id}"
        response = self.api_client.call_api(
            "GET", url, headers=headers, timeout=timeout
        )
        if response.status_code == OK:
            report_content = response.content
        return report_content

    def download_report(
        self,
        report_request: CreateReportDTO,
        path: str,
        max_wait: int = 3600,
        timeout: float = None,
    ) -> Union[str, None]:
        """Generate a report and stream it to ``path`` instead of memory.

        Returns:
            ``path``, or None if the report could not be created or failed.
        """
        report_id = self.create_a_new_report_request(report_request=report_request)
        if not report_id:
            return None
        if not self._wait_until_finished(report_id, max_wait):
            return None
        url = f"{self.base_url}/api/reports/{report_id}"
        return self.api_client.download_to(
            "GET", url, path, headers=headers, timeout=timeout
        )

    def _wait_until_finished(self, report_id: int, max_wait: int) -> bool:
        deadline = time.monotonic() + max_wait
        report_status = self.retrieve_the_status_of_a_specific_report(
            report_id=report_id
        )
        while str(report_status).upper() != "FINISHED":
            if "FAIL" in str(report_status).upper():
                logger.error("Report generation failed!")
                return False
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Report {report_id} not finished within {max_wait}s, "
                    f"last status: {report_status}"
                )
            time.sleep(2)
            report_status = self.retrieve_the_status_of_a_specific_report(
                report_id=report_id
            )
            logger.info("report status: {}".format(report_status))
        return True

    def create_a_new_report_request(
        self, report_request: CreateReportDTO
    ) -> Union[int, None]:
        """

        Args:
            report_request (CreateReportDTO):

        Returns:
            report_id (int)
        """
        report_id = None

        if report_request and not isinstance(report_request, CreateReportDTO):
            return report_id
        url = f"{self.base_url}/api/reports"
        data = json.dumps(report_request.to_dict())
        response = self.api_client.call_api("POST", url, data=data, headers=headers)
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
        url = f"{self.base_url}/api/reports/{report_id}/status"
        response = self.api_client.call_api("GET", url, headers=headers)
        if response.status_code == OK:
            item = response.json()
            report_status = item.get("reportStatus")
        return report_status

    def get_report(
        self,
        report_request: CreateReportDTO,
        max_wait: int = 3600,
        timeout: float = None,
    ) -> Union[bytes, None]:
        """

        Args:
            report_request (CreateReportDTO):
            max_wait (int): maximum seconds to wait for the report.
            timeout (float): per-call timeout in seconds for the download.

        Returns:
            file content (binary string)
        """
        report_id = self.create_a_new_report_request(report_request=report_request)
        if not report_id:
            return None

        report_status = self.retrieve_the_status_of_a_specific_report(
            report_id=report_id
        )
        deadline = time.monotonic() + max_wait
        while str(report_status).upper() != "FINISHED":
            if "FAIL" in str(report_status).upper():
                logger.error("Report generation failed!")
                return None
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Report {report_id} not finished within {max_wait}s, "
                    f"last status: {report_status}"
                )
            report_status = self.retrieve_the_status_of_a_specific_report(
                report_id=report_id
            )
            logger.info("report status: {}".format(report_status))
            time.sleep(2)

        return self.retrieve_the_file_of_a_specific_report(
            report_id=report_id, timeout=timeout
        )


def retrieve_the_file_of_a_specific_report(
    report_id: int, timeout: float = None
) -> bytes:
    return CxReporting().retrieve_the_file_of_a_specific_report(
        report_id=report_id, timeout=timeout
    )


def create_a_new_report_request(report_request: CreateReportDTO) -> int:
    return CxReporting().create_a_new_report_request(report_request=report_request)


def retrieve_the_status_of_a_specific_report(report_id: int) -> str:
    return CxReporting().retrieve_the_status_of_a_specific_report(report_id=report_id)


def get_report(
    report_request: CreateReportDTO, max_wait: int = 3600, timeout: float = None
) -> Union[bytes, None]:
    return CxReporting().get_report(
        report_request=report_request, max_wait=max_wait, timeout=timeout
    )
