import json
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration, get_headers
from datetime import date, datetime, timedelta
from CheckmarxPythonSDK.utilities.compat import OK, ACCEPTED
from .sast.projects.dto import CxLink
from .sast.dataRetention.dto import (
    CxDefineDataRetentionResponse,
    CxDataRetentionRequestStatus,
    CxDataRetentionRequestStatusStage
)


class DataRetentionAPI(object):
    """
    data retention API
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def stop_data_retention(self, api_version: str = "1.0") -> bool:
        """
        Stop the data retention (global)
        Args:
            api_version (str, optional):

        Returns:
            boolean: False

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/sast/dataRetention/stop"
        response = self.api_client.post_request(relative_url=relative_url, data=None, headers=get_headers(api_version))
        if response.status_code == ACCEPTED:
            result = True
        return result

    def define_data_retention_date_range(
            self, start_date: str, end_date: str, duration_limit_in_hours: int, api_version: str = "1.0"
    ) -> CxDefineDataRetentionResponse:
        """
        Define the global setting for data retention by date range

        Args:
            start_date (str): Data retention start date eg. "2019-06-17"
            end_date (str): Data retention end date eg. "2019-06-18"
            duration_limit_in_hours (int): Duration limit (in hours)
            api_version (str, optional):

        Returns:
            CxDefineDataRetentionResponse

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/sast/dataRetention/byDateRange"
        post_data = json.dumps(
            {
                "startDate": start_date,
                "endDate": end_date,
                "durationLimitInHours": duration_limit_in_hours
            }
        )
        response = self.api_client.post_request(
            relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == ACCEPTED:
            if response.text:
                a_dict = response.json()
                result = CxDefineDataRetentionResponse(
                    data_retention_response_id=a_dict.get("id"),
                    link=CxLink(
                        rel=(a_dict.get("link", {}) or {}).get("rel"),
                        uri=(a_dict.get("link", {}) or {}).get("uri")
                    )
                )
        return result

    def define_data_retention_by_number_of_scans(
            self,
            number_of_successful_scans_to_preserve: int,
            duration_limit_in_hours: int,
            api_version: str = "1.0"
    ) -> CxDefineDataRetentionResponse:
        """
        Define the global setting for the data retention by number of scans.

        Args:
            number_of_successful_scans_to_preserve (int): Number of successful scans to keep
            duration_limit_in_hours (int): Duration limit (in hours)
            api_version (str, optional):
        
        Returns:
            CxDefineDataRetentionResponse：
            
        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/sast/dataRetention/byNumberOfScans"
        post_data = json.dumps(
            {
                "numOfSuccessfulScansToPreserve": number_of_successful_scans_to_preserve,
                "durationLimitInHours": duration_limit_in_hours
            }
        )
        response = self.api_client.post_request(
            relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == ACCEPTED:
            if response.text:
                a_dict = response.json()
                result = CxDefineDataRetentionResponse(
                    data_retention_response_id=a_dict.get("id"),
                    link=CxLink(
                        rel=(a_dict.get("link", {}) or {}).get("rel"),
                        uri=(a_dict.get("link", {}) or {}).get("uri")
                    )
                )
        return result

    def get_data_retention_request_status(
            self, request_id: int, api_version: str = "1.0"
    ) -> CxDataRetentionRequestStatus:
        """
        This one does not work!!!
        Get status details of a specific data retention request.

        Args:
            request_id (int): Unique Id of the data retention request.
            api_version (str, optional):

        Returns:
            CxDataRetentionRequestStatus

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/sast/dataRetention/{requestId}/status".format(requestId=request_id)
        response = self.api_client.get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxDataRetentionRequestStatus(
                status_id=a_dict.get("id"),
                stage=CxDataRetentionRequestStatusStage(
                    stage_id=(a_dict.get("stage", {}) or {}).get("id"),
                    value=(a_dict.get("stage", {}) or {}).get("value")
                ),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    def define_data_retention_by_rolling_date(
            self, num_days: int, duration_limit_in_hours: int, api_version: str = "1.0"
    ) -> CxDefineDataRetentionResponse:
        """

        Args:
            num_days (int):
            duration_limit_in_hours (int):
            api_version (str):

        Returns:

        """
        start_date = date(1900, 1, 1).strftime("%Y-%m-%d")
        time_delta = timedelta(days=num_days)
        end_date = (date.today() - time_delta).strftime("%Y-%m-%d")

        return self.define_data_retention_date_range(start_date, end_date, duration_limit_in_hours, api_version)

    def define_data_retention_by_rolling_months(
            self, num_months: int, duration_limit_in_hours: int, api_version: str = "1.0"
    ) -> CxDefineDataRetentionResponse:
        """

        Args:
            num_months (int):
            duration_limit_in_hours (int):
            api_version (str):

        Returns:

        """
        start_date = date(1900, 1, 1)
        start_date = start_date.strftime("%Y-%m-%d")

        today = datetime.now()
        year = today.year
        month = today.month
        month -= num_months
        while month < 1:
            month += 12
            year -= 1
        next_month = month + 1
        next_year = year
        if next_month > 12:
            next_month = 1
            next_year += 1
        end_date = datetime(next_year, next_month, 1) - timedelta(days=1)
        end_date = end_date.strftime("%Y-%m-%d")

        return self.define_data_retention_date_range(start_date, end_date, duration_limit_in_hours, api_version)
