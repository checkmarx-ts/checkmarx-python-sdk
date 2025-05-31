# encoding: utf-8
import json
from .httpRequests import get_request, post_request, patch_request, put_request, delete_request
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT, CREATED
from .utilities import get_url_param, type_check, list_member_type_check
from typing import List
from .dto import (
    ProjectResponseModel,
    SeverityCounter,
    TotalCounters,
    EngineData,
    ProjectCounter,
    ResultsSummaryTree,
    ResultsResponse,
    ResultResponse,
    DebugMessageResponse,
    DebugMessage,
    AsyncRequestResponse,
    SourcesTree,
    QueriesTree,
    QueryRequest,
    Error,
    SessionRequest,
    SessionResponse,
    QueryResponse,
    AuditQuery,
    RequestStatus,
    CompilationResponse,
    ExecutionResponse,
    QueryBuilderMessage,
    QueryBuilderPrompt,
)

server_url = "/api/query-editor"
paths_func_mapping = {
    'create_new_audit_session': '/sessions',
    'heath_check_to_ensure_audit_session_is_kept_alive': '/sessions/{sessionId}',
    'delete_audit_session_with_specific_id': '/sessions/{sessionId}',
    'get_the_logs_associated_to_the_audit_session': '/sessions/{sessionId}/logs',
    'scan_the_audit_session_sources': '/sessions/{sessionId}/sources/scan',
    'create/override_query': '/sessions/{sessionId}/queries',
    'get_all_queries': '/sessions/{sessionId}/queries',
    'get_data_of_a_specified_query': '/sessions/{sessionId}/queries/{editorQueryId}',
    'delete_a_specified_custom_or_overridden_query': '/sessions/{sessionId}/queries/{editorQueryId}',
    'update_specified_query_metadata': '/sessions/{sessionId}/queries/{editorQueryId}/metadata',
    'update_multiple_query_sources': '/sessions/{sessionId}/queries/source',
    'validate_the_queries_provided': '/sessions/{sessionId}/queries/validate',
    'execute_the_queries_on_the_audit_session_scanned_project': '/sessions/{sessionId}/queries/run',
    'check_the_status_of_a_specified_request': '/sessions/{sessionId}/requests/{requestId}',
    'cancel_the_specified_request_execution': '/sessions/{sessionId}/requests/{requestId}/cancel',
    'get_all_results_data_summary_tree_for_all_the_session_runs': '/sessions/{sessionId}/results',
    'get_all_vulnerabilities_related_to_a_given_result': '/sessions/{sessionId}/results/{resultId}/vulnerabilities',
    'get_specified_vulnerability_data_such_as_attack_vector': '/sessions/{sessionId}/results/{resultId}/vulnerabilities'
                                                              '/{vulnerabilityId}',
    'get_specified_result_debug_messages': '/sessions/{sessionId}/results/{resultId}/debug-messages',
    'get_query_builder_history': '/sessions/{sessionId}/gpt',
    'delete_query_builder_gpt_history': '/sessions/{sessionId}/gpt',
    'process_query_builder_gpt_request': '/sessions/{sessionId}/gpt',
}


def create_new_audit_session(request_body: SessionRequest) -> SessionResponse:
    relative_url = server_url + paths_func_mapping.get("create_new_audit_session")
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body.to_dict())
    response = response.json()
    return SessionResponse(
        id=response.get("id"),
        status=response.get("status"),
        scan_id=response.get("scanId"),
    )


def heath_check_to_ensure_audit_session_is_kept_alive(session_id: str) -> bool:
    relative_url = server_url + paths_func_mapping.get("heath_check_to_ensure_audit_session_is_kept_alive").format(
        sessionId=session_id
    )
    params = {}
    response = patch_request(relative_url=relative_url, params=params, json=None)
    return response.status_code == NO_CONTENT


def delete_audit_session_with_specific_id(session_id: str = None) -> bool:
    relative_url = server_url + paths_func_mapping.get("delete_audit_session_with_specific_id").format(
        sessionId=session_id)
    params = {}
    response = delete_request(relative_url=relative_url, params=params)
    return response.status_code == NO_CONTENT


def get_the_logs_associated_to_the_audit_session(session_id: str = None) -> str:
    relative_url = server_url + paths_func_mapping.get("get_the_logs_associated_to_the_audit_session").format(
        sessionId=session_id)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return response


def scan_the_audit_session_sources(session_id: str = None, request_body=None) -> AsyncRequestResponse:
    relative_url = server_url + paths_func_mapping.get("scan_the_audit_session_sources").format(sessionId=session_id)
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    response = response.json()
    return AsyncRequestResponse(
        id=response.get("id"),
    )


def create_or_override_query(request_body: QueryRequest, session_id: str = None) -> AsyncRequestResponse:
    relative_url = server_url + paths_func_mapping.get("create_or_override_query").format(sessionId=session_id)
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    response = response.json()
    return AsyncRequestResponse(
        id=response.get("id"),
    )


def get_all_queries(session_id: str = None, level: str = None, ids: List[str] = None, filters: List[str] = None) \
        -> List[QueriesTree]:
    relative_url = server_url + paths_func_mapping.get("get_all_queries").format(sessionId=session_id)
    params = {"level": level, "ids": ids, "filters": filters}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return [
        QueriesTree(
            is_leaf=item.get("isLeaf"),
            title=item.get("title"),
            key=item.get("key"),
            children=item.get("children"),
        ) for item in response
    ]


def get_data_of_a_specified_query(session_id: str = None, editor_query_id: str = None, include_metadata: bool = None,
                                  include_source: bool = None) -> QueryResponse:
    relative_url = server_url + paths_func_mapping.get("get_data_of_a_specified_query").format(
        sessionId=session_id,
        editorQueryId=editor_query_id,
    )
    params = {"includeMetadata": include_metadata, "includeSource": include_source}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return QueryResponse(
        id=response.get("id"),
        name=response.get("name"),
        level=response.get("level"),
        path=response.get("path"),
        source=response.get("source"),
        metadata=response.get("metadata"),
    )


def delete_a_specified_custom_or_overridden_query(session_id: str, editor_query_id: str) -> AsyncRequestResponse:
    relative_url = server_url + paths_func_mapping.get("delete_a_specified_custom_or_overridden_query").format(
        sessionId=session_id,
        editorQueryId=editor_query_id,
    )
    params = {}
    response = delete_request(relative_url=relative_url, params=params)
    response = response.json()
    return AsyncRequestResponse(
        id=response.get("id"),
    )


def update_specified_query_metadata(severity: str, session_id: str, editor_query_id: str) -> AsyncRequestResponse:
    relative_url = server_url + paths_func_mapping.get("update_specified_query_metadata").format(
        sessionId=session_id,
        editorQueryId=editor_query_id,
    )
    params = {}
    response = put_request(relative_url=relative_url, params=params, json={
      "severity": severity
    })
    response = response.json()
    return AsyncRequestResponse(
        id=response.get("id"),
    )


def update_multiple_query_sources(request_body: List[AuditQuery], session_id: str = None) -> AsyncRequestResponse:
    relative_url = server_url + paths_func_mapping.get("update_multiple_query_sources").format(sessionId=session_id)
    params = {}
    response = put_request(relative_url=relative_url, params=params, json=[item.to_dict() for item in request_body])
    response = response.json()
    return AsyncRequestResponse(
        id=response.get("id"),
    )


def validate_the_queries_provided(request_body: List[AuditQuery], session_id: str = None) -> AsyncRequestResponse:
    relative_url = server_url + paths_func_mapping.get("validate_the_queries_provided").format(sessionId=session_id)
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=[item.to_dict() for item in request_body])
    response = response.json()
    return AsyncRequestResponse(
        id=response.get("id"),
    )


def execute_the_queries_on_the_audit_session_scanned_project(request_body: List[AuditQuery],
                                                             session_id: str = None) -> AsyncRequestResponse:
    relative_url = server_url + paths_func_mapping.get("execute_the_queries_on_the_audit_session_scanned_project"
                                                       ).format(sessionId=session_id)
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=[item.to_dict() for item in request_body])
    response = response.json()
    return AsyncRequestResponse(
        id=response.get("id"),
    )


def check_the_status_of_a_specified_request(session_id: str = None, request_id: str = None) -> RequestStatus:
    relative_url = server_url + paths_func_mapping.get("check_the_status_of_a_specified_request").format(
        sessionId=session_id,
        requestId=request_id,
    )
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return RequestStatus(
        completed=response.get("completed"),
        status=response.get("status"),
        value=response.get("value"),
    )


def cancel_the_specified_request_execution(session_id: str = None, request_id: str = None, request_body=None) -> bool:
    relative_url = server_url + paths_func_mapping.get("cancel_the_specified_request_execution").format(
        sessionId=session_id,
        requestId=request_id,
    )
    params = {}
    response = put_request(relative_url=relative_url, params=params, json=request_body)
    return response.status_code == OK


def get_all_results_data_summary_tree_for_all_the_session_runs(session_id: str = None, run_id: str = None,
                                                               hide_empty: bool = None) -> List[ResultsSummaryTree]:
    relative_url = server_url + paths_func_mapping.get("get_all_results_data_summary_tree_for_all_the_session_runs"
                                                       ).format(sessionId=session_id)
    params = {"runId": run_id, "hideEmpty": hide_empty}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return [
        ResultsSummaryTree(
            is_leaf=item.get("isLeaf"),
            title=item.get("title"),
            key=item.get("key"),
            children=item.get("children"),
            data=item.get("data"),
        ) for item in response
    ]


def get_all_vulnerabilities_related_to_a_given_result(
        session_id: str = None, result_id: str = None, page_size: int = None,
        current_page: int = None) -> ResultsResponse:
    relative_url = server_url + paths_func_mapping.get("get_all_vulnerabilities_related_to_a_given_result").format(
        sessionId=session_id,
        resultId=result_id,
    )
    params = {"pageSize": page_size, "currentPage": current_page}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return ResultsResponse(
        data=response.get("data"),
        total_count=response.get("totalCount"),
    )


def get_specified_vulnerability_data_such_as_attack_vector(session_id: str = None, result_id: str = None,
                                                           vulnerability_id: str = None) -> ResultResponse:
    relative_url = server_url + paths_func_mapping.get("get_specified_vulnerability_data_such_as_attack_vector").format(
        sessionId=session_id,
        resultId=result_id,
        vulnerabilityId=vulnerability_id,
    )
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return ResultResponse(
        vulnerability_id=response.get("vulnerabilityId"),
        source_file=response.get("sourceFile"),
        source_line=response.get("sourceLine"),
        source_id=response.get("sourceId"),
        source_name=response.get("sourceName"),
        source_type=response.get("sourceType"),
        destination_file=response.get("destinationFile"),
        destination_line=response.get("destinationLine"),
        destination_id=response.get("destinationId"),
        destination_name=response.get("destinationName"),
        destination_type=response.get("destinationType"),
        state=response.get("state"),
        path_size=response.get("pathSize"),
    )


def get_specified_result_debug_messages(session_id: str = None, result_id: str = None,
                                        page_size: int = None, current_page: int = None) -> DebugMessageResponse:
    relative_url = server_url + paths_func_mapping.get("get_specified_result_debug_messages").format(
        sessionId=session_id,
        resultId=result_id,
    )
    params = {"pageSize": page_size, "currentPage": current_page}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return DebugMessageResponse(
        data=response.get("data"),
        total_count=response.get("totalCount"),
    )


def get_query_builder_history(session_id: str = None) -> List[QueryBuilderMessage]:
    relative_url = server_url + paths_func_mapping.get("get_query_builder_history").format(sessionId=session_id)
    params = {}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return [
        QueryBuilderMessage(
            role=item.get("role"),
            content=item.get("content"),
        ) for item in response
    ]


def delete_query_builder_gpt_history(session_id: str = None) -> bool:
    relative_url = server_url + paths_func_mapping.get("delete_query_builder_gpt_history").format(sessionId=session_id)
    params = {}
    response = delete_request(relative_url=relative_url, params=params)
    return response.status_code == NO_CONTENT


def process_query_builder_gpt_request(request_body: QueryBuilderPrompt,
                                      session_id: str = None) -> List[QueryBuilderMessage]:
    relative_url = server_url + paths_func_mapping.get("process_query_builder_gpt_request").format(sessionId=session_id)
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    response = response.json()
    return [
        QueryBuilderMessage(
            role=item.get("role"),
            content=item.get("content"),
        ) for item in response
    ]
