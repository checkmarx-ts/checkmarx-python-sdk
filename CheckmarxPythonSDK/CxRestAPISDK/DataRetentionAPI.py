# encoding: utf-8
import requests

from ..compat import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, ACCEPTED
from ..config import config

from . import authHeaders
from .exceptions.CxError import BadRequestError, NotFoundError, CxError
from .sast.projects.dto import CxLink
from .sast.dataRetention.dto import (
    CxDefineDataRetentionNumberOfScansRequest,
    CxDefineDataRetentionResponse,
    CxDefineDataRetentionDateRangeRequest,
    CxDataRetentionRequestStatus,
    CxDataRetentionRequestStatusStage
)


class DataRetentionAPI(object):
    """
    data retention API
    """

    def __init__(self):
        self.retry = 0

    def stop_data_retention(self, api_version="1.0"):
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
        stop_data_retention_url = config.get("base_url") + "/cxrestapi/sast/dataRetention/stop"

        r = requests.post(
            url=stop_data_retention_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == ACCEPTED:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.stop_data_retention(api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def define_data_retention_date_range(self, start_date, end_date, duration_limit_in_hours, api_version="1.0"):
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
        # TODO, check why response content is empty byte
        data_retention = None

        post_body_data = CxDefineDataRetentionDateRangeRequest(
            start_date=start_date,
            end_date=end_date,
            duration_limit_in_hours=duration_limit_in_hours
        ).get_post_data()

        define_data_retention_date_range_url = config.get("base_url") + "/cxrestapi/sast/dataRetention/byDateRange"

        r = requests.post(
            url=define_data_retention_date_range_url,
            data=post_body_data,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == ACCEPTED:
            if r.text:
                a_dict = r.json()
                data_retention = CxDefineDataRetentionResponse(
                    data_retention_response_id=a_dict.get("id"),
                    link=CxLink(
                        rel=(a_dict.get("link", {}) or {}).get("rel"),
                        uri=(a_dict.get("link", {}) or {}).get("uri")
                    )
                )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            data_retention = self.define_data_retention_date_range(start_date, end_date, duration_limit_in_hours,
                                                                   api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return data_retention

    def define_data_retention_by_number_of_scans(self, number_of_successful_scans_to_preserve, duration_limit_in_hours,
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
        # TODO, check why response content is empty byte
        data_retention = None
        post_body_data = CxDefineDataRetentionNumberOfScansRequest(
            number_of_successful_scans_to_preserve=number_of_successful_scans_to_preserve,
            duration_limit_in_hours=duration_limit_in_hours
        ).get_post_data()

        define_data_retention_number_of_scans_url = config.get(
            "base_url") + "/cxrestapi/sast/dataRetention/byNumberOfScans"

        r = requests.post(
            define_data_retention_number_of_scans_url,
            data=post_body_data,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == ACCEPTED:
            if r.text:
                a_dict = r.json()
                data_retention = CxDefineDataRetentionResponse(
                    data_retention_response_id=a_dict.get("id"),
                    link=CxLink(
                        rel=(a_dict.get("link", {}) or {}).get("rel"),
                        uri=(a_dict.get("link", {}) or {}).get("uri")
                    )
                )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            data_retention = self.define_data_retention_by_number_of_scans(number_of_successful_scans_to_preserve,
                                                                           duration_limit_in_hours,
                                                                           api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return data_retention

    def get_data_retention_request_status(self, request_id, api_version="1.0"):
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
        data_retention_request_status_url = config.get(
            "base_url") + "/cxrestapi/sast/dataRetention/{requestId}/status".format(
            requestId=request_id
        )

        r = requests.get(
            url=data_retention_request_status_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            data_detention_request_status = CxDataRetentionRequestStatus(
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
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            data_detention_request_status = self.get_data_retention_request_status(request_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return data_detention_request_status
