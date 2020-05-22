# encoding: utf-8

import requests
import http

from ...config import CxConfig
from ...auth import AuthenticationAPI
from ...exceptions.CxError import BadRequestError, NotFoundError, CxError
from ..projects.dto import CxLink
from .dto import (
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
    
    max_try = CxConfig.CxConfig.config.max_try
    base_url = CxConfig.CxConfig.config.url
    verify = CxConfig.CxConfig.config.verify

    def __init__(self):
        self.retry = 0

    def stop_data_retention(self):
        """
        Stop the data retention (global)

        Returns:
            boolean: False

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        stop_data_retention_url = self.base_url + "/sast/dataRetention/stop"

        r = requests.post(
            url=stop_data_retention_url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
            verify=DataRetentionAPI.verify
        )
        if r.status_code == 202:
            is_successful = True
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.stop_data_retention()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def define_data_retention_date_range(self, start_date, end_date, duration_limit_in_hours):
        """
        Define the global setting for data retention by date range

        Args:
            start_date (str): Data retention start date eg. "2019-06-17"
            end_date (str): Data retention end date eg. "2019-06-18"
            duration_limit_in_hours (int): Duration limit (in hours)

        Returns:
            CxDefineDataRetentionResponse

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        # TODO, check why response content is empty byte
        data_retention = None

        post_body_data = CxDefineDataRetentionDateRangeRequest.CxDefineDataRetentionDateRangeRequest(
            start_date=start_date,
            end_date=end_date,
            duration_limit_in_hours=duration_limit_in_hours
        ).get_post_data()

        define_data_retention_date_range_url = self.base_url + "/sast/dataRetention/byDateRange"

        r = requests.post(
            url=define_data_retention_date_range_url,
            data=post_body_data,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
            verify=DataRetentionAPI.verify
        )

        if r.status_code == 202:
            if r.text:
                a_dict = r.json()
                data_retention = CxDefineDataRetentionResponse.CxDefineDataRetentionResponse(
                    data_retention_response_id=a_dict.get("id"),
                    link=CxLink.CxLink(
                        rel=(a_dict.get("link", {}) or {}).get("rel"),
                        uri=(a_dict.get("link", {}) or {}).get("uri")
                    )
                )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.define_data_retention_date_range(start_date, end_date, duration_limit_in_hours)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return data_retention

    def define_data_retention_by_number_of_scans(self, number_of_successful_scans_to_preserve, duration_limit_in_hours):
        """
        Define the global setting for the data retention by number of scans.

        Args:
            number_of_successful_scans_to_preserve (int): Number of successful scans to keep
            duration_limit_in_hours (int): Duration limit (in hours)
        
        Returns:
            CxDefineDataRetentionResponse：
            
        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        # TODO, check why response content is empty byte
        data_retention = None
        post_body_data = CxDefineDataRetentionNumberOfScansRequest.CxDefineDataRetentionNumberOfScansRequest(
            number_of_successful_scans_to_preserve=number_of_successful_scans_to_preserve,
            duration_limit_in_hours=duration_limit_in_hours
        ).get_post_data()

        define_data_retention_number_of_scans_url = self.base_url + "/sast/dataRetention/byNumberOfScans"

        r = requests.post(
            define_data_retention_number_of_scans_url,
            data=post_body_data,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
            verify=DataRetentionAPI.verify
        )

        if r.status_code == 202:
            if r.text:
                a_dict = r.json()
                data_retention = CxDefineDataRetentionResponse.CxDefineDataRetentionResponse(
                    data_retention_response_id=a_dict.get("id"),
                    link=CxLink.CxLink(
                        rel=(a_dict.get("link", {}) or {}).get("rel"),
                        uri=(a_dict.get("link", {}) or {}).get("uri")
                    )
                )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.define_data_retention_by_number_of_scans(number_of_successful_scans_to_preserve,
                                                          duration_limit_in_hours)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return data_retention

    def get_data_retention_request_status(self, request_id):
        """
        Get status details of a specific data retention request.
        :param request_id: int
        :return:

        Args:
            request_id (int): Unique Id of the data retention request.
        
        Returns:
            CxDataRetentionRequestStatus
        
        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        data_detention_request_status = None

        data_retention_request_status_url = self.base_url + "/sast/dataRetention/{requestId}/status".format(
            requestId=request_id
        )

        r = requests.get(
            url=data_retention_request_status_url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
            verify=DataRetentionAPI.verify
        )

        if r.status_code == 200:
            a_dict = r.json()
            data_detention_request_status = CxDataRetentionRequestStatus.CxDataRetentionRequestStatus(
                status_id=a_dict.get("id"),
                stage=CxDataRetentionRequestStatusStage.CxDataRetentionRequestStatusStage(
                    stage_id=(a_dict.get("stage", {}) or {}).get("id"),
                    value=(a_dict.get("stage", {}) or {}).get("value")
                ),
                link=CxLink.CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_data_retention_request_status(request_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return data_detention_request_status
