# encoding: utf-8
import json
import datetime
from dateutil.relativedelta import relativedelta
from .httpRequests import get_request, post_request, get_headers
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
    @staticmethod
    def stop_data_retention(api_version="1.0"):
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
        response = post_request(relative_url=relative_url, data=None, headers=get_headers(api_version))
        if response.status_code == ACCEPTED:
            result = True
        return result

    @staticmethod
    def define_data_retention_date_range(start_date, end_date, duration_limit_in_hours, api_version="1.0"):
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
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
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

    @staticmethod
    def define_data_retention_by_number_of_scans(number_of_successful_scans_to_preserve, duration_limit_in_hours,
                                                 api_version="1.0"):
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
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
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

    @staticmethod
    def get_data_retention_request_status(request_id, api_version="1.0"):
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
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
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

    @staticmethod
    def define_data_retention_by_rolling_date(num_days, duration_limit_in_hours, api_version="1.0"):
        """

        Args:
            num_days (int):
            duration_limit_in_hours (int):
            api_version (str):

        Returns:

        """
        start_date = datetime.date(1900, 1, 1)
        start_date = start_date.strftime("%Y-%m-%d")

        time_delta = datetime.timedelta(days=num_days)
        end_date = datetime.date.today() - time_delta
        end_date = end_date.strftime("%Y-%m-%d")

        return DataRetentionAPI.define_data_retention_date_range(start_date, end_date, duration_limit_in_hours,
                                                                 api_version)

    @staticmethod
    def define_data_retention_by_rolling_months(num_months, duration_limit_in_hours, api_version="1.0"):
        """

        Args:
            num_months (int):
            duration_limit_in_hours (int):
            api_version (str):

        Returns:

        """
        start_date = datetime.date(1900, 1, 1)
        start_date = start_date.strftime("%Y-%m-%d")

        the_last_day_of_this_month = datetime.date.today() + relativedelta(day=31)
        end_date = the_last_day_of_this_month - relativedelta(months=num_months) + relativedelta(day=31)
        end_date = end_date.strftime("%Y-%m-%d")

        return DataRetentionAPI.define_data_retention_date_range(start_date, end_date, duration_limit_in_hours,
                                                                 api_version)
