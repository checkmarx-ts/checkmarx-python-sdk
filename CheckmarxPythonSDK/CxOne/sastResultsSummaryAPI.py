from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class SastResultsSummaryAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/sast-scan-summary"
        )

    def get_sast_aggregate_results(
        self,
        scan_id: str,
        group_by_field: List[str],
        apply_predicates: bool = True,
        attack_vector_id: str = None,
        bfl_group_size: int = None,
        bfl_group_size_operation: str = None,
        bfl_name: str = None,
        bfl_name_operation: str = None,
        categories: str = None,
        confidence_level: int = None,
        confidence_level_operation: str = None,
        confidence_score: int = None,
        confidence_score_operation: str = None,
        cwe_id: int = None,
        cwe_id_operation: str = None,
        first_found_at: str = None,
        first_found_at_operation: str = None,
        group: str = None,
        group_operation: str = None,
        is_ai_generated: int = None,
        is_ai_generated_operation: str = None,
        language: List[str] = None,
        limit: int = 20,
        notes: str = None,
        notes_operation: str = None,
        number_of_nodes: int = None,
        number_of_nodes_operation: str = None,
        offset: int = 0,
        preset_id: str = None,
        query: str = None,
        query_ids: List[int] = None,
        query_operation: str = None,
        result_ids: List[str] = None,
        search: str = None,
        severity: List[str] = None,
        similarity_id: int = None,
        similarity_id_operation: str = None,
        sink_file: str = None,
        sink_file_operation: str = None,
        sink_line: int = None,
        sink_line_operation: str = None,
        sink_node: str = None,
        sink_node_operation: str = None,
        source_file: str = None,
        source_file_operation: str = None,
        source_line: int = None,
        source_line_operation: str = None,
        source_node: str = None,
        source_node_operation: str = None,
        status: List[str] = None,
        correlation_id: str = None,
    ) -> dict:
        """GET /api/sast-scan-summary/aggregate -- aggregated summary of
        SAST results for a scan. An AND operator is applied between
        filters, and an OR operator between multiple values of the
        same filter.

        Args:
            scan_id (str): Required. Filter by scan id.
            group_by_field (list of str): Required. Fields to group
                results. Values: QUERY, SEVERITY, STATE, STATUS,
                SOURCE_NODE, SINK_NODE, SOURCE_FILE, SINK_FILE,
                LANGUAGE, CWE.
            apply_predicates (bool): If true, results account for
                predicate changes; if false, based on raw predicate
                values. Default: true.
            attack_vector_id (str): Filter by attack vector id (exact
                match only).
            bfl_group_size (int): Filter by BFL group size.
            bfl_group_size_operation (str): LESS_THAN, GREATER_THAN,
                EQUAL, NOT_EQUAL.
            bfl_name (str): Filter by BFL name.
            bfl_name_operation (str): CONTAINS, START_WITH.
            categories (str): Comma-separated list of category names.
            confidence_level (int): Filter by confidence level.
            confidence_level_operation (str): LESS_THAN, GREATER_THAN,
                EQUAL, NOT_EQUAL.
            confidence_score (int): Filter by confidence score.
            confidence_score_operation (str): LESS_THAN, GREATER_THAN,
                EQUAL, NOT_EQUAL.
            cwe_id (int): Filter by CWE id.
            cwe_id_operation (str): LESS_THAN, GREATER_THAN, EQUAL,
                NOT_EQUAL.
            first_found_at (str): Filter by first-found-at (RFC3339
                date-time).
            first_found_at_operation (str): LESS_THAN, GREATER_THAN.
            group (str): Filter by vulnerability group. Can be a
                substring of the group name.
            group_operation (str): CONTAINS, START_WITH.
            is_ai_generated (int): Filter by AI-generated flag: 1 for
                AI (LAST) results, 0 for traditional SAST results
                (matches the results endpoint's isAiGenerated field).
            is_ai_generated_operation (str): LESS_THAN, GREATER_THAN,
                EQUAL, NOT_EQUAL.
            language (list of str): Filter by language (case-insensitive,
                exact match).
            limit (int): Max results, 1-10000. Default: 20.
            notes (str): Filter by last notes.
            notes_operation (str): LESS_THAN, GREATER_THAN, EQUAL,
                NOT_EQUAL, CONTAINS, NOT_CONTAINS, START_WITH.
            number_of_nodes (int): Filter by number of nodes.
            number_of_nodes_operation (str): LESS_THAN, GREATER_THAN,
                EQUAL, NOT_EQUAL.
            offset (int): Results to skip. Default: 0.
            preset_id (str): Filter by preset.
            query (str): Filter by query name. Can be a substring of
                the query name.
            query_ids (list of int): Filter by query ids.
            query_operation (str): LESS_THAN, GREATER_THAN, EQUAL,
                NOT_EQUAL, CONTAINS, NOT_CONTAINS, START_WITH.
            result_ids (list of str): Filter by unique result hashes.
            search (str): Filter by source file name, source node,
                sink node, sink file name, or notes.
            severity (list of str): Filter by severity. Values:
                CRITICAL, HIGH, MEDIUM, LOW, INFO.
            similarity_id (int): Filter by similarity id.
            similarity_id_operation (str): LESS_THAN, GREATER_THAN,
                EQUAL, NOT_EQUAL.
            sink_file (str): Filter by sink file name.
            sink_file_operation (str): LESS_THAN, GREATER_THAN, EQUAL,
                NOT_EQUAL, CONTAINS, NOT_CONTAINS, START_WITH.
            sink_line (int): Filter by sink line.
            sink_line_operation (str): LESS_THAN, GREATER_THAN, EQUAL,
                NOT_EQUAL.
            sink_node (str): Filter by sink node.
            sink_node_operation (str): LESS_THAN, GREATER_THAN, EQUAL,
                NOT_EQUAL, CONTAINS, NOT_CONTAINS, START_WITH.
            source_file (str): Filter by source file name.
            source_file_operation (str): LESS_THAN, GREATER_THAN,
                EQUAL, NOT_EQUAL, CONTAINS, NOT_CONTAINS, START_WITH.
            source_line (int): Filter by source line.
            source_line_operation (str): LESS_THAN, GREATER_THAN,
                EQUAL, NOT_EQUAL.
            source_node (str): Filter by source node.
            source_node_operation (str): LESS_THAN, GREATER_THAN,
                EQUAL, NOT_EQUAL, CONTAINS, NOT_CONTAINS, START_WITH.
            status (list of str): Filter by status. Values: NEW,
                RECURRENT.
            correlation_id (str): Optional UUID, for internal
                Checkmarx use.

        Returns:
            dict
        """
        url = f"{self.base_url}/aggregate"
        params = {
            "scan-id": scan_id,
            "group-by-field": group_by_field,
            "apply-predicates": apply_predicates,
            "attack-vector-id": attack_vector_id,
            "bfl-group-size": bfl_group_size,
            "bfl-group-size-operation": bfl_group_size_operation,
            "bfl-name": bfl_name,
            "bfl-name-operation": bfl_name_operation,
            "categories": categories,
            "confidence-level": confidence_level,
            "confidence-level-operation": confidence_level_operation,
            "confidence-score": confidence_score,
            "confidence-score-operation": confidence_score_operation,
            "cwe-id": cwe_id,
            "cwe-id-operation": cwe_id_operation,
            "first-found-at": first_found_at,
            "first-found-at-operation": first_found_at_operation,
            "group": group,
            "group-operation": group_operation,
            "is-ai-generated": is_ai_generated,
            "is-ai-generated-operation": is_ai_generated_operation,
            "language": language,
            "limit": limit,
            "notes": notes,
            "notes-operation": notes_operation,
            "number-of-nodes": number_of_nodes,
            "number-of-nodes-operation": number_of_nodes_operation,
            "offset": offset,
            "preset-id": preset_id,
            "query": query,
            "query-ids": query_ids,
            "query-operation": query_operation,
            "result-ids": result_ids,
            "search": search,
            "severity": severity,
            "similarity-id": similarity_id,
            "similarity-id-operation": similarity_id_operation,
            "sink-file": sink_file,
            "sink-file-operation": sink_file_operation,
            "sink-line": sink_line,
            "sink-line-operation": sink_line_operation,
            "sink-node": sink_node,
            "sink-node-operation": sink_node_operation,
            "source-file": source_file,
            "source-file-operation": source_file_operation,
            "source-line": source_line,
            "source-line-operation": source_line_operation,
            "source-node": source_node,
            "source-node-operation": source_node_operation,
            "status": status,
        }
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers,
        )
        return response.json()

    def get_sast_aggregate_results_comparison(
        self,
        scan_id: str,
        base_scan_id: str,
        group_by_field: List[str],
        language: List[str] = None,
        status: List[str] = None,
        severity: List[str] = None,
        query_ids: List[int] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict:
        """
        Args:
            scan_id (str): Scan ID of the newer scan to compare.
            base_scan_id (str): Scan ID of the older scan to compare.
            group_by_field (List[str]): Group by parameters.
                Values: LANGUAGE, QUERY
            language (List[str]): Filter by language (exact,
                case-insensitive).
            status (List[str]): Filter by status.
                Values: NEW, RECURRENT, FIXED
            severity (List[str]): Filter by severity.
                Values: CRITICAL, HIGH, MEDIUM, LOW, INFO
            query_ids (List[int]): Filter by query IDs.
            limit (int): Maximum results. Default: 20.
            offset (int): Results to skip. Default: 0.

        Returns:
            dict
        """
        url = f"{self.base_url}/compare/aggregate"
        params = {
            "scan-id": scan_id,
            "base-scan-id": base_scan_id,
            "group-by-field": group_by_field,
            "language": language,
            "status": status,
            "severity": severity,
            "query-ids": query_ids,
            "limit": limit,
            "offset": offset,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()


def get_sast_aggregate_results(
    scan_id: str,
    group_by_field: List[str],
    apply_predicates: bool = True,
    attack_vector_id: str = None,
    bfl_group_size: int = None,
    bfl_group_size_operation: str = None,
    bfl_name: str = None,
    bfl_name_operation: str = None,
    categories: str = None,
    confidence_level: int = None,
    confidence_level_operation: str = None,
    confidence_score: int = None,
    confidence_score_operation: str = None,
    cwe_id: int = None,
    cwe_id_operation: str = None,
    first_found_at: str = None,
    first_found_at_operation: str = None,
    group: str = None,
    group_operation: str = None,
    is_ai_generated: int = None,
    is_ai_generated_operation: str = None,
    language: List[str] = None,
    limit: int = 20,
    notes: str = None,
    notes_operation: str = None,
    number_of_nodes: int = None,
    number_of_nodes_operation: str = None,
    offset: int = 0,
    preset_id: str = None,
    query: str = None,
    query_ids: List[int] = None,
    query_operation: str = None,
    result_ids: List[str] = None,
    search: str = None,
    severity: List[str] = None,
    similarity_id: int = None,
    similarity_id_operation: str = None,
    sink_file: str = None,
    sink_file_operation: str = None,
    sink_line: int = None,
    sink_line_operation: str = None,
    sink_node: str = None,
    sink_node_operation: str = None,
    source_file: str = None,
    source_file_operation: str = None,
    source_line: int = None,
    source_line_operation: str = None,
    source_node: str = None,
    source_node_operation: str = None,
    status: List[str] = None,
    correlation_id: str = None,
) -> dict:
    return SastResultsSummaryAPI().get_sast_aggregate_results(
        scan_id=scan_id,
        group_by_field=group_by_field,
        apply_predicates=apply_predicates,
        attack_vector_id=attack_vector_id,
        bfl_group_size=bfl_group_size,
        bfl_group_size_operation=bfl_group_size_operation,
        bfl_name=bfl_name,
        bfl_name_operation=bfl_name_operation,
        categories=categories,
        confidence_level=confidence_level,
        confidence_level_operation=confidence_level_operation,
        confidence_score=confidence_score,
        confidence_score_operation=confidence_score_operation,
        cwe_id=cwe_id,
        cwe_id_operation=cwe_id_operation,
        first_found_at=first_found_at,
        first_found_at_operation=first_found_at_operation,
        group=group,
        group_operation=group_operation,
        is_ai_generated=is_ai_generated,
        is_ai_generated_operation=is_ai_generated_operation,
        language=language,
        limit=limit,
        notes=notes,
        notes_operation=notes_operation,
        number_of_nodes=number_of_nodes,
        number_of_nodes_operation=number_of_nodes_operation,
        offset=offset,
        preset_id=preset_id,
        query=query,
        query_ids=query_ids,
        query_operation=query_operation,
        result_ids=result_ids,
        search=search,
        severity=severity,
        similarity_id=similarity_id,
        similarity_id_operation=similarity_id_operation,
        sink_file=sink_file,
        sink_file_operation=sink_file_operation,
        sink_line=sink_line,
        sink_line_operation=sink_line_operation,
        sink_node=sink_node,
        sink_node_operation=sink_node_operation,
        source_file=source_file,
        source_file_operation=source_file_operation,
        source_line=source_line,
        source_line_operation=source_line_operation,
        source_node=source_node,
        source_node_operation=source_node_operation,
        status=status,
        correlation_id=correlation_id,
    )


def get_sast_aggregate_results_comparison(
    scan_id: str,
    base_scan_id: str,
    group_by_field: List[str],
    language: List[str] = None,
    status: List[str] = None,
    severity: List[str] = None,
    query_ids: List[int] = None,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    return SastResultsSummaryAPI().get_sast_aggregate_results_comparison(
        scan_id=scan_id,
        base_scan_id=base_scan_id,
        group_by_field=group_by_field,
        language=language,
        status=status,
        severity=severity,
        query_ids=query_ids,
        limit=limit,
        offset=offset,
    )
