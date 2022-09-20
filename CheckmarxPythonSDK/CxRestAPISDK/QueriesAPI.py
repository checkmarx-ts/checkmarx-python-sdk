# encoding: utf-8
from .httpRequests import get_request, get_headers
from CheckmarxPythonSDK.utilities.compat import OK


class QueriesAPI(object):

    @staticmethod
    def get_the_full_description_of_the_query(query_id, api_version="3.0"):
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
        result = None
        relative_url = "/cxrestapi/queries/{queryid}/cxDescription".format(queryid=query_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result
