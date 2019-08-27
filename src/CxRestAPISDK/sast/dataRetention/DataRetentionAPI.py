# encoding: utf-8

import requests
import http


from src.CxRestAPISDK.config import CxConfig
from src.CxRestAPISDK.auth import AuthenticationAPI

from src.CxRestAPISDK.sast.dataRetention.dto import (CxDefineDataRetentionNumberOfScansRequest,
                                                     CxDefineDataRetentionResponse,
                                                     CxDefineDataRetentionDateRangeRequest,
                                                     CxDataRetentionRequestStatus,
                                                     CxDataRetentionRequestStatusStage)
from src.CxRestAPISDK.sast.projects.dto import CxLink
from src.CxRestAPISDK.exceptions.CxError import BadRequestError, NotFoundError, UnknownHttpStatusError


class DataRetentionAPI(object):
    """
    data retention API
    """
    
    max_try = CxConfig.CxConfig.config.max_try
    base_url = CxConfig.CxConfig.config.url

    stop_data_retention_url = base_url + "/sast/dataRetention/stop"
    define_data_retention_date_range_url = base_url + "/sast/dataRetention/byDateRange"
    define_data_retention_number_of_scans_url = base_url + "/sast/dataRetention/byNumberOfScans"

    data_retention_request_status_url = base_url + "/sast/dataRetention/{requestId}/status"

    def __init__(self):
        self.retry = 0

    def stop_data_retention(self):
        """
        Stop the data retention (global)

        Returns:
            bool: False

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        is_successful = False
        r = requests.post(url=self.stop_data_retention_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
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
            raise UnknownHttpStatusError()
        return is_successful

    def define_data_retention_date_range(self, start_date, end_date, duration_limit_in_hours):
        """
        Define the global setting for data retention by date range

        Args:
            start_date (str): eg. "2019-06-17"
            end_date (str): eg. "2019-06-18"
            duration_limit_in_hours (int):

        Returns:
            CxDefineDataRetentionResponse

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        data_retention = None

        post_body_data = CxDefineDataRetentionDateRangeRequest.CxDefineDataRetentionDateRangeRequest(
            start_date=start_date,
            end_date=end_date,
            duration_limit_in_hours=duration_limit_in_hours
        ).get_post_data()

        r = requests.post(url=self.define_data_retention_date_range_url, data=post_body_data,
                          headers=AuthenticationAPI.AuthenticationAPI.auth_headers)

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
            raise UnknownHttpStatusError()
        return data_retention

    def define_data_retention_by_number_of_scans(self, number_of_successful_scans_to_preserve, duration_limit_in_hours):
        """
        Define the global setting for the data retention by number of scans.

        Args:
            number_of_successful_scans_to_preserve (int): 
            duration_limit_in_hours (int):
        
        Returns:
            CxDefineDataRetentionResponse：
            
        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        data_retention = None
        post_body_data = CxDefineDataRetentionNumberOfScansRequest.CxDefineDataRetentionNumberOfScansRequest(
            number_of_successful_scans_to_preserve=number_of_successful_scans_to_preserve,
            duration_limit_in_hours=duration_limit_in_hours
        ).get_post_data()

        r = requests.post(self.define_data_retention_number_of_scans_url, data=post_body_data,
                          headers=AuthenticationAPI.AuthenticationAPI.auth_headers)

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
            raise UnknownHttpStatusError()
        return data_retention

    def get_data_retention_request_status(self, request_id):
        """
        Get status details of a specific data retention request.
        :param request_id: int
        :return:

        Args:
            request_id (int):
        
        Returns:
            CxDataRetentionRequestStatus
        
        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        data_detention_request_status = None
        self.data_retention_request_status_url = self.data_retention_request_status_url.format(requestId=request_id)
        r = requests.get(url=self.data_retention_request_status_url,
                         headers=AuthenticationAPI.AuthenticationAPI.auth_headers)

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
            raise UnknownHttpStatusError()

        return data_detention_request_status
