from .httpRequests import get_request, post_request, patch_request, delete_request
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED, OK
from typing import List
from deprecated import deprecated


server_url = "/api/sast-results-predicates"
paths_func_mapping = {
    'get_all_predicates_for_similarity_id': '/{similarityID}',
    'get_latest_predicates_for_similarity_id': '/{similarityID}/latest',
    'predicate_severity_and_state_by_similarity_id_and_project_id': '/',
    'update_predicate_comment_by_predicate_id': '/',
    'recalculate_summary_counters': '/recalculateSummaryCounters',
    'delete_a_predicate_history': '/{similarityID}/{projectID}/{predicateID}'
}


def get_all_predicates_for_similarity_id(
        similarity_id: str,
        project_ids: List[str] = None,
        include_comment_json: bool = None,
        scan_id: str = None) -> dict:
    relative_url = server_url + paths_func_mapping.get(
        "get_all_predicates_for_similarity_id").format(similarityID=similarity_id)
    params = {"project-ids": project_ids, "include-comment-json": include_comment_json, "scan-id": scan_id}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return response


def get_latest_predicates_for_similarity_id(
        similarity_id: str, project_ids: List[str] = None, scan_id: str = None) -> dict:
    relative_url = server_url + paths_func_mapping.get(
        "get_latest_predicates_for_similarity_id").format(similarityID=similarity_id)
    params = {"project-ids": project_ids, "scan-id": scan_id}
    response = get_request(relative_url=relative_url, params=params)
    response = response.json()
    return response


def predicate_severity_and_state_by_similarity_id_and_project_id(
        request_body: List[dict]) -> bool:
    relative_url = server_url + paths_func_mapping.get("predicate_severity_and_state_by_similarity_id_and_project_id")
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    return response.status_code == CREATED


@deprecated(version='1.2.6', reason='This endpoint is not supported')
def update_predicate_comment_by_predicate_id(request_body: List[dict]) -> bool:
    relative_url = server_url + paths_func_mapping.get("update_predicate_comment_by_predicate_id")
    params = {}
    response = patch_request(relative_url=relative_url, params=params, json=request_body)
    return response.status_code == NO_CONTENT


def recalculate_summary_counters(request_body: dict) -> bool:
    relative_url = server_url + paths_func_mapping.get("recalculate_summary_counters")
    params = {}
    response = post_request(relative_url=relative_url, params=params, json=request_body)
    return response.status_code == OK


@deprecated(version='1.2.6', reason='This endpoint is not supported')
def delete_a_predicate_history(similarity_id: str, project_id: str, predicate_id: str) -> bool:
    relative_url = server_url + paths_func_mapping.get("delete_a_predicate_history").format(
        similarityID=similarity_id,
        projectID=project_id,
        predicateID=predicate_id
    )
    params = {}
    response = delete_request(relative_url=relative_url, params=params)
    return response.status_code == NO_CONTENT
