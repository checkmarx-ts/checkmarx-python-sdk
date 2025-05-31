from typing import List
from .httpRequests import get_request, post_request, put_request, delete_request
from .dto import (
    Queries,
    Query,
    QuerySearch,
    MethodInfo,
    MethodParameter,
    QueryRequest,
    WorkspaceQuery,
    SessionRequest,
    SessionResponse,
    Sessions,
    Session,
    SastStatus,
    RequestStatusNotReady,
    RequestStatusDetectLanguages,
    AuditQuery,
    CompilationResponse,
    ExecutionResponse,
    GPTMessage
)

from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, OK

server_url = "/api/cx-audit"
paths_func_mapping = {
    'get_all_queries': '/queries',
    'create_new_query': '/query-editor/sessions/{session_id}/queries',
    'get_all_queries_search': '/queries/{session_id}/search',
    'get_queries_metadata': '/queries/metadata',
    'get_query_source': '/queries/{level}/{path}',
    'delete_overridden_query': '/queries/{level}/{path}',
    'update_query_source': '/queries/{session_id}/{level}',
    'create_new_session': '/sessions',
    'get_all_active_sessions_related_to_webaudit': '/sessions',
    'get_session_details': '/sessions/{id}',
    'delete_session_with_specific_id': '/sessions/{session_id}',
    'heath_check_to_ensure_session_is_kept_alive': '/sessions/{session_id}',
    'check_if_sast_engine_is_ready_to_use': '/sessions/{session_id}/sast-status',
    'check_the_status_of_some_scan_related_requests': '/sessions/{session_id}/request-status',
    'detect_the_languages_of_the_project_to_scan': '/sessions/{session_id}/project/languages',
    'scan_the_project_using_sast_engine': '/sessions/{session_id}/project/scan',
    'compile_the_queries_of_the_scanned_project': '/sessions/{session_id}/queries/compile',
    'execute_the_queries_of_the_scanned_project': '/sessions/{session_id}/queries/run',
    'cancel_the_queries_execution': '/sessions/{session_id}/queries/cancel',
    'get_the_logs_associated_to_the_audit_session': '/sessions/{session_id}/logs',
    'retrieve_gpt_history': '/gpt/{session_id}',
    'delete_gpt_history': '/gpt/{session_id}',
    'process_gpt_prompt_request': '/gpt/{session_id}'
}


def get_all_queries(project_id: str = None) -> List[Queries]:
    relative_url = server_url + paths_func_mapping.get("get_all_queries")
    params = {"projectId": project_id}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return [
        Queries(
            id=item.get("Id"),
            name=item.get("name"),
            group=item.get("group"),
            level=item.get("level"),
            lang=item.get("lang"),
            is_executable=item.get("isExecutable"),
        ) for item in response
    ]


def create_new_query(session_id: str, request_body: QueryRequest) -> bool:
    relative_url = server_url + paths_func_mapping.get("create_new_query").format(session_id=session_id)
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    return response.status_code == OK


def get_all_queries_search(session_id: str) -> List[QuerySearch]:
    relative_url = server_url + paths_func_mapping.get("get_all_queries_search").format(session_id=session_id)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return [
        QuerySearch(
            query=item.get("query"),
            results=item.get("results"),
        ) for item in response
    ]


def get_queries_metadata() -> List[MethodInfo]:
    relative_url = server_url + paths_func_mapping.get("get_queries_metadata")
    params = {}
    response = get_request(relative_url=relative_url, params=params)
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


def get_query_source(level: str, path: str) -> Query:
    relative_url = server_url + paths_func_mapping.get("get_query_source").format(level=level, path=path)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return Query(
        id=response.get("id"),
        source=response.get("source"),
        level=response.get("level"),
        path=response.get("path"),
        modified=response.get("modified"),
        cwe=response.get("cwe"),
        severity=response.get("severity"),
        is_executable=response.get("isExecutable"),
        cx_description_id=response.get("cxDescriptionID"),
        query_description_id=response.get("queryDescriptionID"),
    )


def delete_overridden_query(level: str, path: str) -> bool:
    relative_url = server_url + paths_func_mapping.get("delete_overridden_query").format(level=level, path=path)
    params = {}
    response = delete_request(relative_url=relative_url, params=params)
    return response.status_code == NO_CONTENT


def update_query_source(request_body: List[WorkspaceQuery], session_id: str, level: str) -> bool:
    relative_url = server_url + paths_func_mapping.get("update_query_source").format(session_id=session_id, level=level)
    params = {}
    response = put_request(relative_url=relative_url, params=params, json=request_body)
    return response.status_code == OK


def create_new_session(request_body: SessionRequest) -> SessionResponse:
    relative_url = server_url + paths_func_mapping.get("create_new_session")
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    response = response.json()
    return SessionResponse(
        id=response.get("id"),
        status=response.get("status"),
        scan_id=response.get("scanId"),
    )


def get_all_active_sessions_related_to_webaudit(project_id: str = None, scan_id: str = None) -> Sessions:
    relative_url = server_url + paths_func_mapping.get("get_all_active_sessions_related_to_webaudit")
    params = {"projectId": project_id, "scanId": scan_id}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return Sessions(
        available=response.get("available"),
        metadata=response.get("metadata"),
    )


def get_session_details(session_id: str) -> Session:
    relative_url = server_url + paths_func_mapping.get("get_session_details").format(session_id=session_id)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return Session(
        session_id=response.get("session_id"),
        tenant_id=response.get("tenant_id"),
        project_id=response.get("project_id"),
        source_id=response.get("source_id"),
        worker_info=response.get("worker_info"),
        status=response.get("status"),
    )


def delete_session_with_specific_id(session_id: str) -> bool:
    relative_url = server_url + paths_func_mapping.get("delete_session_with_specific_id").format(session_id=session_id)
    params = {}
    response = delete_request(relative_url=relative_url, params=params)
    return response.status_code == NO_CONTENT


def heath_check_to_ensure_session_is_kept_alive(session_id: str, request_body=None) -> bool:
    relative_url = server_url + paths_func_mapping.get("heath_check_to_ensure_session_is_kept_alive").format(
        session_id=session_id)
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    return response.status_code == NO_CONTENT


def check_if_sast_engine_is_ready_to_use(session_id: str) -> SastStatus:
    relative_url = server_url + paths_func_mapping.get("check_if_sast_engine_is_ready_to_use").format(
        session_id=session_id)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return SastStatus(
        ready=response.get("ready"),
        message=response.get("message"),
    )


def check_the_status_of_some_scan_related_requests(session_id: str, status_type: int):
    relative_url = server_url + paths_func_mapping.get("check_the_status_of_some_scan_related_requests").format(
        session_id=session_id)
    params = {"type": status_type}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return response


def detect_the_languages_of_the_project_to_scan(session_id: str) -> int:
    relative_url = server_url + paths_func_mapping.get("detect_the_languages_of_the_project_to_scan").format(
        session_id=session_id)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return response


def scan_the_project_using_sast_engine(session_id: str) -> int:
    relative_url = server_url + paths_func_mapping.get("scan_the_project_using_sast_engine").format(
        session_id=session_id)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return response


def compile_the_queries_of_the_scanned_project(request_body: List[AuditQuery], session_id: str) -> int:
    relative_url = server_url + paths_func_mapping.get("compile_the_queries_of_the_scanned_project").format(
        session_id=session_id)
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    response = response.json()
    return response


def execute_the_queries_of_the_scanned_project(request_body: List[AuditQuery], session_id: str) -> int:
    relative_url = server_url + paths_func_mapping.get("execute_the_queries_of_the_scanned_project").format(
        session_id=session_id)
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    response = response.json()
    return response


def cancel_the_queries_execution(session_id: str) -> bool:
    relative_url = server_url + paths_func_mapping.get("cancel_the_queries_execution").format(session_id=session_id)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    return response.status_code == OK


def get_the_logs_associated_to_the_audit_session(session_id: str) -> str:
    relative_url = server_url + paths_func_mapping.get("get_the_logs_associated_to_the_audit_session").format(
        session_id=session_id)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return response


def retrieve_gpt_history(session_id: str) -> List[GPTMessage]:
    relative_url = server_url + paths_func_mapping.get("retrieve_gpt_history").format(session_id=session_id)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return [
        GPTMessage(
            role=item.get("role"),
            content=item.get("content"),
        ) for item in response
    ]


def delete_gpt_history(session_id: str) -> bool:
    relative_url = server_url + paths_func_mapping.get("delete_gpt_history").format(session_id=session_id)
    params = {}
    response = delete_request(relative_url=relative_url, params=params)
    return response.status_code == NO_CONTENT


def process_gpt_prompt_request(request_body: dict, session_id: str) -> List[GPTMessage]:
    relative_url = server_url + paths_func_mapping.get("process_gpt_prompt_request").format(session_id=session_id)
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    response = response.json()
    return [
        GPTMessage(
            role=item.get("role"),
            content=item.get("content"),
        ) for item in response
    ]
