from .httpRequests import get_request, post_request, put_request, delete_request
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED, OK
from typing import Any, List
from .dto import(
    StateEnum,
    SeverityEnum,
    PredicateHistory,
    Predicate,
    PredicateWithCommentJSON,
    PredicateWitCommentsJSON,
    CommentJSON,
    WebError
)


server_url = "/api/query-editor"
paths_func_mapping = {'get_all_predicates_for_similarity_id': '/{similarityID}', 'get_latest_predicates_for_similarity_id': '/{similarityID}/latest', 'predicate_severity_and_state_by_similiarty_id_and_project_id': '/', 'update_predicate_comment_by_predicate_id': '/', 'recalculate_summary_counters': '/recalculateSummaryCounters', 'delete_a_predicate_history': '/{similarityID}/{projectID}/{predicateID}'}


def get_all_predicates_for_similarity_id(auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None, similarity_id: str, project_ids: List[str] = None, include_comment_json: bool = None, scan_id: str = None) -> dict:
    relative_url = server_url + paths_func_mapping.get("get_all_predicates_for_similarity_id")
    params = {"authHeader": auth_header, "versionHeader": version_header, "correlationIdHeader": correlation_id_header, "similarityID": similarity_id, "project-ids": project_ids, "include-comment-json": include_comment_json, "scan-id": scan_id}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return response


def get_latest_predicates_for_similarity_id(auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None, similarity_id: str, project_ids: List[str] = None, scan_id: str = None) -> dict:
    relative_url = server_url + paths_func_mapping.get("get_latest_predicates_for_similarity_id")
    params = {"authHeader": auth_header, "versionHeader": version_header, "correlationIdHeader": correlation_id_header, "similarityID": similarity_id, "project-ids": project_ids, "scan-id": scan_id}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return response


def predicate_severity_and_state_by_similiarty_id_and_project_id(request_body: List[dict], auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None) -> bool:
    relative_url = server_url + paths_func_mapping.get("predicate_severity_and_state_by_similiarty_id_and_project_id")
    params = {"authHeader": auth_header, "versionHeader": version_header, "correlationIdHeader": correlation_id_header}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    return response.status_code == CREATED


def update_predicate_comment_by_predicate_id(request_body: List[dict], auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None) -> bool:
    relative_url = server_url + paths_func_mapping.get("update_predicate_comment_by_predicate_id")
    params = {"authHeader": auth_header, "versionHeader": version_header, "correlationIdHeader": correlation_id_header}
    response = patch_request(relative_url=relative_url, params=params, json=request_body)
    return response.status_code == NO_CONTENT


def recalculate_summary_counters(request_body: dict, auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None) -> bool:
    relative_url = server_url + paths_func_mapping.get("recalculate_summary_counters")
    params = {"authHeader": auth_header, "versionHeader": version_header, "correlationIdHeader": correlation_id_header}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    return response.status_code == ACCEPTED


def delete_a_predicate_history(auth_header: authHeader = None, version_header: versionHeader = None, correlation_id_header: correlationIdHeader = None, similarity_id: str, project_id: str, predicate_id: str) -> bool:
    relative_url = server_url + paths_func_mapping.get("delete_a_predicate_history")
    params = {"authHeader": auth_header, "versionHeader": version_header, "correlationIdHeader": correlation_id_header, "similarityID": similarity_id, "projectID": project_id, "predicateID": predicate_id}
    response = delete_request(relative_url=relative_url, params=params)
    return response.status_code == NO_CONTENT

