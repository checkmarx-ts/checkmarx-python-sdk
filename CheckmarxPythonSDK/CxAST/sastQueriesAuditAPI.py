from .httpRequests import get_request, put_request
from .utilities import get_url_param, type_check
from .dto import Queries, Query, MethodParameter, MethodInfo, WorkspaceQuery
from CheckmarxPythonSDK.utilities.compat import OK

query_url = "/api/cx-audit"


def get_all_queries(project_id=None):
    """

    Args:
        project_id (str):

    Returns:

    """
    type_check(project_id, str)

    relative_url = query_url + "/queries"
    if project_id:
        relative_url += "?"
    relative_url += get_url_param("projectId", project_id)
    response = get_request(relative_url=relative_url)
    response = response.json()
    return [
        Queries(
            name=item.get("name"),
            group=item.get("group"),
            level=item.get("level"),
            lang=item.get("lang"),
            path=item.get("path"),
            modify=item.get("modify"),
            is_executable=item.get("isExecutable")
        ) for item in response
    ]


def get_queries_metadata():
    relative_url = query_url + "/queries/metadata"
    response = get_request(relative_url=relative_url)
    response = response.json()
    return [
        MethodInfo(
            lang=item.get("lang"),
            name=item.get("name"),
            member_of=item.get("memberOf"),
            documentation=item.get("documentation"),
            return_type=item.get("returnType"),
            kind=item.get("kind"),
            parameters=[
                MethodParameter(
                    name=m.get("name"),
                    label=m.get("label"),
                    documentation=m.get("documentation"),
                ) for m in item.get("parameters") or []
            ]
        ) for item in response
    ]


def get_query_source(level, path):
    """

    Args:
        level (str): corp or projectId
        path (str): queries%2FCommon%2FCommon_High_Risk%2FSQL_Injection%2FSQL_Injectio.cs

    Returns:

    """
    type_check(level, str)
    type_check(path, str)

    relative_url = query_url + "/query/{level}/{path}".format(level=level, path=path)
    response = get_request(relative_url=relative_url)
    response = response.json()
    return Query(
        source=response.get("source"),
        level=response.get("level"),
        path=response.get("path"),
        modified=response.get("modified"),
        cwe=response.get("Cwe"),
        severity=response.get("Severity"),
        is_executable=response.get("IsExecutable"),
        cx_description_id=response.get("CxDescriptionID"),
        query_description_id=response.get("QueryDescriptionID"),
    )


def update_query_source(level, workspace_query):
    """

    Args:
        level (str): corp or projectId
        workspace_query (WorkspaceQuery):

    Returns:

    """
    type_check(level, str)
    type_check(workspace_query, WorkspaceQuery)

    is_successful = False
    relative_url = query_url + "/queries/{level}".format(level=level)
    data = workspace_query.get_post_data()
    response = put_request(relative_url=relative_url, data=data)
    if response.status_code == OK:
        is_successful = True
    return is_successful
