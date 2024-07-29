# encoding: utf-8
import json
from .httpRequests import get_request, post_request, patch_request, put_request, delete_request
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import (
    ProjectResponseModel,
    SeverityCounter,
    TotalCounters,
    EngineData,
    ProjectCounter,
)

api_url = "/api/query-editor"


def create_new_audit_session(project_id, scan_id, upload_url, timeout=30, scanner="sast"):
    """

    Args:
        project_id (str):
        scan_id (str):
        scanner (str):
        timeout (int):
        upload_url (str):

    Returns:

    """
    result = None
    type_check(project_id, str)
    type_check(scan_id, str)
    type_check(scanner, str)
    type_check(timeout, int)
    type_check(upload_url, str)

    relative_url = api_url + "/sessions"
    data = json.dumps(
        {
            "projectId": project_id,
            "scanId": scan_id,
            "scanner": scanner,
            "timeout": timeout,
            "uploadUrl": upload_url,
        }
    )
    response = post_request(relative_url=relative_url, data=data)
    if response.status_code == OK:
        result = response.json()
    return result
    #     result = {
    #         "id": "a888aa5a-d207-4ad0-8bfa-0743d6ca0e0d",
    #         "data": {
    #             "requestId": "a888aa5a-d207-4ad0-8bfa-0743d6ca0e0d",
    #             "status": "Status_ALLOCATED",
    #             "queryFilters": [
    #                 "Java",
    #                 "Javascript",
    #                 "Common"
    #             ],
    #             "queryBuilder": True,
    #             "applicationAssociation": False,
    #             "projectName": "JavaVulnerabilities_Project",
    #             "permissions": {
    #                 "tenant": {
    #                     "view": True,
    #                     "update": True,
    #                     "create": True,
    #                     "delete": True
    #                 },
    #                 "application": {
    #                     "view": False,
    #                     "update": False,
    #                     "create": False,
    #                     "delete": False
    #                 },
    #                 "project": {
    #                     "view": True,
    #                     "update": True,
    #                     "create": True,
    #                     "delete": True
    #                 }
    #             }
    #         }
    #     }
    # return result


def health_check_audit_session(session_id):
    """
    Heath check to ensure Audit session is kept alive
    Args:
        session_id (str):

    Returns:

    """
    is_successful = False
    type_check(session_id, str)

    relative_url = api_url + "/sessions/{sessionId}".format(sessionId=session_id)
    response = patch_request(relative_url=relative_url, data="")
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def delete_audit_session(session_id):
    """
    Delete Audit session with specific id
    Args:
        session_id (str):

    Returns:

    """
    is_successful = False
    type_check(session_id, str)

    relative_url = api_url + "/sessions/{sessionId}".format(sessionId=session_id)
    response = delete_request(relative_url=relative_url)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def get_audit_session_log(session_id):
    """

    Args:
        session_id (str):

    Returns:

    """
    result = None
    type_check(session_id, str)

    relative_url = api_url + "/sessions/{sessionId}/logs".format(sessionId=session_id)
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        result = response.content
    return result


def scan_audit_session_sources(session_id):
    """
    Scan the Audit Session sources
    Args:
        session_id (str):

    Returns:

    """
    result = None
    type_check(session_id, str)
    relative_url = api_url + "/sessions/{sessionId}/sources/scan".format(sessionId=session_id)
    response = post_request(relative_url=relative_url, data="")
    if response.status_code == NO_CONTENT:
        result = response.json().get("id")
    return result


def create_or_override_query(session_id, query_name, language, group, severity, executable, preset, cwe, description):
    """
    create/override query
    Args:
        session_id (str):
        query_name (str):
        language (str):
        group (str):
        severity (str):
        executable (bool):
        preset (list of str):
        cwe (int):
        description (str):

    Returns:

    """
    result = None
    type_check(session_id, str)
    type_check(query_name, str)
    type_check(language, str)
    type_check(group, str)
    type_check(severity, str)
    type_check(executable, bool)
    type_check(preset, list)
    list_member_type_check(preset, str)
    type_check(cwe, int)
    type_check(description, str)

    relative_url = api_url + "/sessions/{sessionId}/queries".format(sessionId=session_id)
    data = json.dumps(
        {
            "name": query_name,
            "language": language,
            "group": group,
            "severity": severity,
            "executable": True,
            "presets": preset,
            "cwe": cwe,
            "description": description,
        }
    )
    response = post_request(relative_url=relative_url, data=data)
    if response.status_code == OK:
        result = response.json().get("id")
    return result


def get_all_queries(session_id):
    """

    Args:
        session_id (str):

    Returns:

    """
    result = None
    type_check(session_id, str)
    relative_url = api_url + "/sessions/{sessionId}/queries".format(sessionId=session_id)
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        result = response.json()
        #
        # [
        #     {
        #         "isLeaf": false,
        #         "title": "JavaScript",
        #         "key": "javascript",
        #         "children": [
        #             {
        #                 "isLeaf": false,
        #                 "title": "Tenant",
        #                 "key": "tenant",
        #                 "children": [
        #                     {
        #                         "isLeaf": false,
        #                         "title": "Common_Best_Coding_Practice",
        #                         "key": "Common_Best_Coding_Practice",
        #                         "children": [
        #                             {
        #                                 "isLeaf": true,
        #                                 "title": "Assigning_instead_of_Comparing",
        #                                 "key": "IFZXG2LHNZUW4Z27NFXHG5DFMFSF633GL5BW63LQMFZGS3TH",
        #                                 "children": []
        #                             },
        #                             {
        #                                 "isLeaf": true,
        #                                 "title": "Comparing_instead_of_Assigning",
        #                                 "key": "INXW24DBOJUW4Z27NFXHG5DFMFSF633GL5AXG43JM5XGS3TH",
        #                                 "children": []
        #                             },
        #                             {
        #                                 "isLeaf": true,
        #                                 "title": "Declaration_Of_Catch_For_Generic_Exception",
        #                                 "key": "IRSWG3DBOJQXI2LPNZPU6ZS7INQXIY3IL5DG64S7I5SW4ZLSNFRV6RLYMNSXA5DJN5XA",
        #                                 "children": []
        #                             },
        #                             {
        #                                 "isLeaf": true,
        #                                 "title": "Detection_Of_Error_Condition_Without_Action",
        #                                 "key": "IRSXIZLDORUW63S7J5TF6RLSOJXXEX2DN5XGI2LUNFXW4X2XNF2GQ33VORPUCY3UNFXW4",
        #                                 "children": []
        #                             },
        #                             {
        #                                 "isLeaf": true,
        #                                 "title": "Hardcoded_Absolute_Path",
        #                                 "key": "JBQXEZDDN5SGKZC7IFRHG33MOV2GKX2QMF2GQ",
        #                                 "children": []
        #                             },
        #                             {
        #                                 "isLeaf": true,
        #                                 "title": "Insufficient_Logging_Of_Database_Actions",
        #                                 "key": "JFXHG5LGMZUWG2LFNZ2F6TDPM5TWS3THL5HWMX2EMF2GCYTBONSV6QLDORUW63TT",
        #                                 "children": []
        #                             }
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # ]
    return result


def get_data_of_specific_query(session_id, editor_query_id, include_metadata=False, include_source=False):
    """

    Args:
        session_id (str):
        editor_query_id (str):
        include_metadata (bool):  Parameter to define if the metadata object should be included in the response.
        include_source (bool): Parameter to define if the source of the query object should be included in the response.

    Returns:

    """
    result = None
    type_check(session_id, str)
    type_check(editor_query_id, str)
    type_check(include_metadata, bool)
    type_check(include_source, bool)

    relative_url = api_url + ("/sessions/{sessionId}/queries/{editorQueryId}"
                              "?includeMetadata={includeMetadata}&includeSource={includeSource}").format(
        sessionId=session_id, editorQueryId=editor_query_id, includeMetadata=include_metadata,
        includeSource=include_source
    )
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        result = response.json()
        # result = {
        #     "id": "2syswoof68vqZkernrZQJhjb9QwRZ4VxooQaVsFxbf3q0zQnGvjiVDev200INh08i3SircSio8adEE4G9niVbPZeA",
        #     "name": "SQL_Injection",
        #     "level": "project",
        #     "path": "CSharp/CSharp_High_Risk/SQL_Injection",
        #     "source": "result = Find_SQL_Injection();",
        #     "metadata": {
        #         "group": "CSharp_Low_Visibility",
        #         "severity": "high",
        #         "language": "CSharp",
        #         "cwe": 566,
        #         "description": 879,
        #         "executable": true
        #     }
        # }
    return result


def delete_a_specific_query(session_id, editor_query_id):
    """

    Args:
        session_id (str):
        editor_query_id (str):

    Returns:

    """
    result = None
    type_check(session_id, str)
    type_check(editor_query_id, str)
    relative_url = api_url + "/sessions/{sessionId}/queries/{editorQueryId}".format(
        sessionId=session_id, editorQueryId=editor_query_id
    )
    response = delete_request(relative_url=relative_url)
    if response.status_code == OK:
        result = response.json().get("id")
    return result


def update_specified_query_metadata(session_id, editor_query_id, severity):
    """

    Args:
        session_id (str):
        editor_query_id (str):
        severity (str): "Critical"

    Returns:

    """
    result = None
    type_check(session_id, str)
    type_check(editor_query_id, str)
    relative_url = api_url + "/sessions/{sessionId}/queries/{editorQueryId}/metadata".format(
        sessionId=session_id, editorQueryId=editor_query_id
    )
    data = json.dumps(
        {
            "severity": severity
        }
    )
    response = put_request(relative_url=relative_url, data=data)
    if response.status_code == OK:
        result = response.json().get("id")
    return result


def update_multiple_query_sources(session_id, audit_queries):
    """

    Args:
        session_id (str):
        audit_queries (AuditQueries):

    Returns:
        str
    """

