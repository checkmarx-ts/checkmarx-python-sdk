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

    @staticmethod
    def get_query_id_and_query_version_code(language, query_name, severity="High", api_version="4.0"):
        """

        Args:
            language (str): Language of the query
            query_name (str): Severity of the query, default value is "Info"
            severity (str): Query name of the query
            api_version (str, optional):

        Returns:
            dict
            example:
            {
              "queryId": 0,
              "queryVersionCode": 0
            }
        """
        result = None
        relative_url = "/cxrestapi/queries/queryVersionCode?"
        checkmarx_supported_languages = [
            "Apex", "ASP", "Cobol", "CPP", "CSharp", "Dart", "Go", "Groovy", "Java", "JavaScript", "Kotlin", "Lua",
            "Objc", "Perl", "PHP", "PLSQL", "Python", "RPG", "Ruby", "Rust", "Scala", "Swift", "VB6", "VbNet",
            'VbScript'
        ]
        severity_list = ["High", "Medium", "Low", "Info"]
        if language and language not in checkmarx_supported_languages:
            raise ValueError(
                "language wrong value, supported languages: {}".format(",".join(checkmarx_supported_languages))
            )
        if severity and severity not in severity_list:
            raise ValueError(
                "severity wrong value, supported severity: {}".format(",".join(severity_list))
            )
        relative_url += "language={language}&severity={severity}&queryName={query_name}".format(
            language=language, severity=severity, query_name=query_name
        )
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result

    @staticmethod
    def get_preset_detail(preset_id, api_version="5.0"):
        """
        Gets query information of specific preset
        Args:
            preset_id (int):
            api_version (str):

        Returns:
            list of dict
            example:
            [
              {
                "queryId": 0,
                "queryName": "string",
                "queryLanguage": "string",
                "querySource": "string"
              }
            ]
        """
        result = None
        relative_url = "/cxrestapi/sast/presetDetails/{id}".format(id=preset_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result
