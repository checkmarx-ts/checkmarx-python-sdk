# encoding: utf-8
import os
import json
import copy

import requests

from requests_toolbelt import MultipartEncoder

from ..compat import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, CREATED, ACCEPTED, NO_CONTENT
from ..config import config

from . import authHeaders
from .TeamAPI import TeamAPI
from .exceptions.CxError import BadRequestError, NotFoundError, CxError


class QueriesAPI(object):

    def __init__(self):
        self.retry = 0

    def get_the_full_description_of_the_query(self, query_id, api_version="3.0"):
        """

        Args:
            query_id (int):
            api_version (str, optional):

        Returns:
            str

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        url = config.get("base_url") + "/cxrestapi/queries/{queryid}/cxDescription".format(queryid=query_id)

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            description = r.json()
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            description = self.get_the_full_description_of_the_query(query_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return description


