from typing import List

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED, OK, ACCEPTED
from .dto import (
    LatestPredicateResponse,
    PredicateHistoryResponse,
    PredicatesChangelogResponse,
    PredicatesStatus,
)


class SastResultsPredicatesAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/sast-results-predicates"
        )

    def get_all_predicates_for_similarity_id(
        self,
        similarity_id: str,
        project_ids: List[str] = None,
        include_comment_json: bool = None,
        include_changed_by: bool = None,
        scan_id: str = None,
        offset: int = 0,
        limit: int = 100,
        correlation_id: str = None,
    ) -> PredicateHistoryResponse:
        """GET /api/sast-results-predicates/{similarityID} -- all SAST
        predicates (state/severity/comment history) for a vulnerability
        instance.

        Args:
            similarity_id (str): Required.
            project_ids (list of str): Filter by project (OR between
                items). Default: all projects.
            include_comment_json (bool): Include comment data.
            include_changed_by (bool): Include triggeredBy/changedBy
                info on each predicate.
            scan_id (str): Filter by scan.
            offset (int): Results to skip. Default: 0.
            limit (int): Max results. Default: 100.
            correlation_id (str): Optional UUID, for internal
                Checkmarx use.

        Returns:
            PredicateHistoryResponse
        """
        url = f"{self.base_url}/{similarity_id}"
        params = {
            "project-ids": project_ids,
            "include-comment-json": include_comment_json,
            "include-changed-by": include_changed_by,
            "scan-id": scan_id,
            "offset": offset,
            "limit": limit,
        }
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers,
        )
        return PredicateHistoryResponse.from_dict(response.json())

    def get_latest_predicates_for_similarity_id(
        self,
        similarity_id: str,
        project_ids: List[str] = None,
        scan_id: str = None,
        include_changed_by: bool = None,
        correlation_id: str = None,
    ) -> LatestPredicateResponse:
        """GET /api/sast-results-predicates/{similarityID}/latest --
        the latest predicate per project for a vulnerability instance.

        Args:
            similarity_id (str): Required.
            project_ids (list of str): Filter by project (OR between
                items). Default: all projects.
            scan_id (str): Filter by scan.
            include_changed_by (bool): Include triggeredBy/changedBy
                info on each predicate. Not observed to have any
                effect on this endpoint's response on a live tenant
                (unlike the plain /{similarityID} endpoint, where it
                does) -- still sent through in case that's
                data-dependent rather than a genuine no-op.
            correlation_id (str): Optional UUID, for internal
                Checkmarx use.

        Returns:
            LatestPredicateResponse
        """
        url = f"{self.base_url}/{similarity_id}/latest"
        params = {
            "project-ids": project_ids,
            "scan-id": scan_id,
            "include-changed-by": include_changed_by,
        }
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers,
        )
        return LatestPredicateResponse.from_dict(response.json())

    def predicate_severity_and_state_by_similarity_id_and_project_id(
        self,
        data: List[dict],
        allow_ai_triage_cancellation: bool = None,
        correlation_id: str = None,
    ) -> bool:
        """POST /api/sast-results-predicates/ -- change the predicate
        (severity/state/comment) for one or more vulnerability
        instances.

        Args:
            data (list of dict): Each item needs similarityId,
                projectId, severity, state, comment (required, may be
                empty string), and optionally scanId.
            allow_ai_triage_cancellation (bool): If an AI Triage
                analysis is currently queued/in_progress for any
                target vulnerability, the request fails with 409
                (code 4092) unless this is true, in which case active
                AI Triage jobs are cancelled, their reserved credits
                returned, and this manual update applied immediately.
                Default: false.
            correlation_id (str): Optional UUID, for internal
                Checkmarx use.

        Returns:
            bool: True if the update was successful (201).
        """
        url = f"{self.base_url}/"
        params = {
            "allowAITriageCancellation": allow_ai_triage_cancellation,
        }
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        response = self.api_client.call_api(
            method="POST", url=url, params=params, json=data, headers=headers,
        )
        return response.status_code == CREATED

    def update_predicate_comment_by_predicate_id(
        self, data: List[dict]
    ) -> bool:
        """
        Args:
            data (list of dict):

        Returns:
            bool
        """
        url = f"{self.base_url}/"
        response = self.api_client.call_api(
            method="PATCH", url=url, json=data
        )
        return response.status_code == NO_CONTENT

    def recalculate_summary_counters(
        self, data: dict, correlation_id: str = None
    ) -> bool:
        """POST /api/sast-results-predicates/recalculateSummaryCounters
        -- fix a scan's results summary to reflect the actual number
        of results.

        Args:
            data (dict): {"projectId": str (required), "scanId": str
                (optional)}. When scanId is given, processed
                synchronously (200) and this call waits until it
                completes; when omitted, processed asynchronously
                (202) and this call returns immediately once queued
                -- both are success.
            correlation_id (str): Optional UUID, for internal
                Checkmarx use.

        Returns:
            bool
        """
        url = f"{self.base_url}/recalculateSummaryCounters"
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        response = self.api_client.call_api(
            method="POST", url=url, json=data, headers=headers,
        )
        return response.status_code in (OK, ACCEPTED)

    def delete_a_predicate_history(
        self, similarity_id: str, project_id: str, predicate_id: str
    ) -> bool:
        """
        Args:
            similarity_id (str):
            project_id (str):
            predicate_id (str):

        Returns:
            bool
        """
        url = (
            f"{self.base_url}/{similarity_id}/{project_id}/{predicate_id}"
        )
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def get_predicates_by_attack_vector_id(
        self,
        attack_vector_id: str,
        similarity_id: str = None,
        project_ids: List[str] = None,
        scan_id: str = None,
        include_comment_json: bool = None,
        include_changed_by: bool = None,
        offset: int = 0,
        limit: int = 100,
        correlation_id: str = None,
    ) -> PredicateHistoryResponse:
        """GET /api/sast-results-predicates/ -- predicates applied to
        a specific attack vector.

        Args:
            attack_vector_id (str): Required. 16-char hex ID of the
                attack vector.
            similarity_id (str): Filter by similarity ID.
            project_ids (List[str]): Filter by project IDs (OR between
                items). Default: all projects.
            scan_id (str): Filter by scan ID.
            include_comment_json (bool): Include comment JSON data.
            include_changed_by (bool): Include triggeredBy/changedBy
                info on each predicate.
            offset (int): Results to skip. Default: 0.
            limit (int): Max results, 1-100. Default: 100.
            correlation_id (str): Optional UUID, for internal
                Checkmarx use.

        Returns:
            PredicateHistoryResponse
        """
        url = f"{self.base_url}/"
        params = {
            "attack-vector-id": attack_vector_id,
            "similarity-id": similarity_id,
            "project-ids": project_ids,
            "scan-id": scan_id,
            "include-comment-json": include_comment_json,
            "include-changed-by": include_changed_by,
            "offset": offset,
            "limit": limit,
        }
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers,
        )
        return PredicateHistoryResponse.from_dict(response.json())

    def get_predicates_changelog(
        self,
        entity_type: str,
        entity_id: str,
        history: bool = False,
        offset: int = 0,
        limit: int = 100,
        correlation_id: str = None,
    ) -> PredicatesChangelogResponse:
        """GET /api/sast-results-predicates/changelog -- bulk
        predicates for a similarityID, scanID, or projectID.

        Note: the public doc's response schema shows `results` as a
        flat array of change entries ({change, date, user, origin}).
        The live response actually groups them by similarityId --
        results[{similarityId, predicates: [{change, date, user,
        origin}], totalCount}] -- as modeled by PredicatesChangelogResponse.

        Args:
            entity_type (str): One of 'similarityID', 'scanID', 'projectID'.
            entity_id (str): The ID value of the selected entity type.
            history (bool): True = full history; False = latest state
                only (observed live: this can still return multiple
                entries per similarity id, just fewer than with
                history=True -- it's not strictly "one entry").
            offset (int): Results to skip. Default: 0.
            limit (int): Max results (1-100). Default: 100.
            correlation_id (str): Optional UUID, for internal
                Checkmarx use.

        Returns:
            PredicatesChangelogResponse
        """
        url = f"{self.base_url}/changelog"
        params = {
            "entityType": entity_type,
            "entityId": entity_id,
            "history": history,
            "offset": offset,
            "limit": limit,
        }
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers,
        )
        return PredicatesChangelogResponse.from_dict(response.json())

    def create_predicates_by_attack_vector(
        self,
        data: List[dict],
        allow_ai_triage_cancellation: bool = None,
        correlation_id: str = None,
    ) -> bool:
        """POST /api/sast-results-predicates/attack-vector -- create a
        predicate entry for SAST results sharing a common attack
        vector. Supports bulk creation across all similarity groups
        sharing the attack vector, or a targeted update for one via
        filterBySimilarityId.

        Args:
            data (List[dict]): Each item needs attackVectorId
                (16-char hex) and projectId. Optional: scanId, state,
                severity, comment (<=1024 chars), customStateId,
                filterBySimilarityId, allowInconsistentStates (if the
                attack vector's similarity groups have different
                states applied, the request fails unless this is
                true).
            allow_ai_triage_cancellation (bool): If an AI Triage
                analysis is currently queued/in_progress for any
                target vulnerability, the request fails with 409
                (code 4092) unless this is true, in which case active
                AI Triage jobs are cancelled, their reserved credits
                returned, and this manual update applied immediately.
                Default: false.
            correlation_id (str): Optional UUID, for internal
                Checkmarx use.

        Returns:
            bool
        """
        url = f"{self.base_url}/attack-vector"
        params = {
            "allowAITriageCancellation": allow_ai_triage_cancellation,
        }
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        response = self.api_client.call_api(
            method="POST", url=url, params=params, json=data, headers=headers,
        )
        return response.status_code == CREATED

    def get_predicates_status(
        self,
        scan_id: str,
        similar_results_ids: List[str],
        correlation_id: str = None,
    ) -> PredicatesStatus:
        """POST /api/sast-results-predicates/predicates-status --
        monitoring endpoint to check whether a bulk update-predicates
        process (e.g. AI Triage) is currently running for a set of
        similarity/attack-vector IDs within a scan, and which
        grouping mode ("Similarity ID" or "Attack Vector ID") this
        tenant is configured to use.

        Args:
            scan_id (str): Scan ID to check.
            similar_results_ids (List[str]): Similarity IDs or attack
                vector IDs to check (max 200).
            correlation_id (str): Optional UUID, for internal
                Checkmarx use.

        Returns:
            PredicatesStatus
        """
        url = f"{self.base_url}/predicates-status"
        body = {"scanID": scan_id, "similarResultsIDs": similar_results_ids}
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        response = self.api_client.call_api(
            method="POST", url=url, json=body, headers=headers,
        )
        return PredicatesStatus.from_dict(response.json())


def get_all_predicates_for_similarity_id(
    similarity_id: str,
    project_ids: List[str] = None,
    include_comment_json: bool = None,
    include_changed_by: bool = None,
    scan_id: str = None,
    offset: int = 0,
    limit: int = 100,
    correlation_id: str = None,
) -> PredicateHistoryResponse:
    return SastResultsPredicatesAPI().get_all_predicates_for_similarity_id(
        similarity_id=similarity_id,
        project_ids=project_ids,
        include_comment_json=include_comment_json,
        include_changed_by=include_changed_by,
        scan_id=scan_id,
        offset=offset,
        limit=limit,
        correlation_id=correlation_id,
    )


def get_latest_predicates_for_similarity_id(
    similarity_id: str,
    project_ids: List[str] = None,
    scan_id: str = None,
    include_changed_by: bool = None,
    correlation_id: str = None,
) -> LatestPredicateResponse:
    return SastResultsPredicatesAPI().get_latest_predicates_for_similarity_id(
        similarity_id=similarity_id,
        project_ids=project_ids,
        scan_id=scan_id,
        include_changed_by=include_changed_by,
        correlation_id=correlation_id,
    )


def predicate_severity_and_state_by_similarity_id_and_project_id(
    data: List[dict],
    allow_ai_triage_cancellation: bool = None,
    correlation_id: str = None,
) -> bool:
    return SastResultsPredicatesAPI().predicate_severity_and_state_by_similarity_id_and_project_id(
        data=data,
        allow_ai_triage_cancellation=allow_ai_triage_cancellation,
        correlation_id=correlation_id,
    )


def update_predicate_comment_by_predicate_id(data: List[dict]) -> bool:
    return SastResultsPredicatesAPI().update_predicate_comment_by_predicate_id(
        data=data
    )


def recalculate_summary_counters(
    data: dict, correlation_id: str = None
) -> bool:
    return SastResultsPredicatesAPI().recalculate_summary_counters(
        data=data, correlation_id=correlation_id
    )


def delete_a_predicate_history(
    similarity_id: str, project_id: str, predicate_id: str
) -> bool:
    return SastResultsPredicatesAPI().delete_a_predicate_history(
        similarity_id=similarity_id,
        project_id=project_id,
        predicate_id=predicate_id,
    )


def get_predicates_by_attack_vector_id(
    attack_vector_id: str,
    similarity_id: str = None,
    project_ids: List[str] = None,
    scan_id: str = None,
    include_comment_json: bool = None,
    include_changed_by: bool = None,
    offset: int = 0,
    limit: int = 100,
    correlation_id: str = None,
) -> PredicateHistoryResponse:
    return SastResultsPredicatesAPI().get_predicates_by_attack_vector_id(
        attack_vector_id=attack_vector_id,
        similarity_id=similarity_id,
        project_ids=project_ids,
        scan_id=scan_id,
        include_comment_json=include_comment_json,
        include_changed_by=include_changed_by,
        offset=offset,
        limit=limit,
        correlation_id=correlation_id,
    )


def get_predicates_changelog(
    entity_type: str,
    entity_id: str,
    history: bool = False,
    offset: int = 0,
    limit: int = 100,
    correlation_id: str = None,
) -> PredicatesChangelogResponse:
    return SastResultsPredicatesAPI().get_predicates_changelog(
        entity_type=entity_type,
        entity_id=entity_id,
        history=history,
        offset=offset,
        limit=limit,
        correlation_id=correlation_id,
    )


def create_predicates_by_attack_vector(
    data: List[dict],
    allow_ai_triage_cancellation: bool = None,
    correlation_id: str = None,
) -> bool:
    return SastResultsPredicatesAPI().create_predicates_by_attack_vector(
        data=data,
        allow_ai_triage_cancellation=allow_ai_triage_cancellation,
        correlation_id=correlation_id,
    )


def get_predicates_status(
    scan_id: str,
    similar_results_ids: List[str],
    correlation_id: str = None,
) -> PredicatesStatus:
    return SastResultsPredicatesAPI().get_predicates_status(
        scan_id=scan_id,
        similar_results_ids=similar_results_ids,
        correlation_id=correlation_id,
    )
