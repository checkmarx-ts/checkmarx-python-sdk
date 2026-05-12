from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT
from typing import List
from .dto import (
    ResultsSummaryTree,
    ResultsResponse,
    ResultResponse,
    DebugMessageResponse,
    AsyncRequestResponse,
    QueriesTree,
    QueryRequest,
    SessionRequest,
    SessionResponse,
    QueryResponse,
    AuditQuery,
    RequestStatus,
    QueryBuilderMessage,
    QueryBuilderPrompt,
)


class QueryEditorAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            "/api/query-editor"
        )

    def create_new_audit_session(
        self, data: SessionRequest
    ) -> SessionResponse:
        """
        Args:
            data (SessionRequest):

        Returns:
            SessionResponse
        """
        url = f"{self.base_url}/sessions"
        response = self.api_client.call_api(
            method="POST", url=url,
            json={k: v for k, v in asdict(data).items() if v is not None}
        )
        return SessionResponse.from_dict(response.json())

    def heath_check_to_ensure_audit_session_is_kept_alive(
        self, session_id: str
    ) -> bool:
        """
        Args:
            session_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/sessions/{session_id}"
        response = self.api_client.call_api(method="PATCH", url=url)
        return response.status_code == NO_CONTENT

    def delete_audit_session_with_specific_id(
        self, session_id: str
    ) -> bool:
        """
        Args:
            session_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/sessions/{session_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def get_the_logs_associated_to_the_audit_session(
        self, session_id: str
    ) -> bytes:
        """
        Args:
            session_id (str):

        Returns:
            bytes
        """
        url = f"{self.base_url}/sessions/{session_id}/logs"
        response = self.api_client.call_api(method="GET", url=url)
        return response.content

    def scan_the_audit_session_sources(
        self, session_id: str
    ) -> AsyncRequestResponse:
        """
        Args:
            session_id (str):

        Returns:
            AsyncRequestResponse
        """
        url = f"{self.base_url}/sessions/{session_id}/sources/scan"
        response = self.api_client.call_api(method="POST", url=url)
        return AsyncRequestResponse.from_dict(response.json())

    def create_or_override_query(
        self, data: QueryRequest, session_id: str
    ) -> AsyncRequestResponse:
        """
        Args:
            data (QueryRequest):
            session_id (str):

        Returns:
            AsyncRequestResponse
        """
        url = f"{self.base_url}/sessions/{session_id}/queries"
        response = self.api_client.call_api(
            method="POST", url=url,
            json={k: v for k, v in asdict(data).items() if v is not None}
        )
        return AsyncRequestResponse.from_dict(response.json())

    def get_all_queries(
        self,
        session_id: str,
        level: str = None,
        ids: List[str] = None,
        filters: List[str] = None,
    ) -> List[QueriesTree]:
        """
        Args:
            session_id (str): The session ID.
            level (str): Parameter to filter queries by its level.
            ids (List[str]): Parameter to filter queries by its IDs.
            filters (List[str]): Filters for queries. Language on SAST
                or Technology on IaC.

        Returns:
            List[QueriesTree]
        """
        url = f"{self.base_url}/sessions/{session_id}/queries"
        params = {"level": level, "ids": ids, "filters": filters}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return [
            QueriesTree.from_dict(item) for item in (response.json() or [])
        ]

    def get_data_of_a_specified_query(
        self,
        session_id: str,
        editor_query_id: str,
        include_metadata: bool = False,
        include_source: bool = False,
    ) -> QueryResponse:
        """
        Args:
            session_id (str): The session ID.
            editor_query_id (str):
            include_metadata (bool): If true, include the metadata
                object in the response.
            include_source (bool): If true, include the source of the
                query object in the response.

        Returns:
            QueryResponse
        """
        url = (
            f"{self.base_url}/sessions/{session_id}"
            f"/queries/{editor_query_id}"
        )
        params = {
            "includeMetadata": include_metadata,
            "includeSource": include_source,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return QueryResponse.from_dict(response.json())

    def delete_a_specified_custom_or_overridden_query(
        self, session_id: str, editor_query_id: str
    ) -> AsyncRequestResponse:
        """
        Args:
            session_id (str):
            editor_query_id (str):

        Returns:
            AsyncRequestResponse
        """
        url = (
            f"{self.base_url}/sessions/{session_id}"
            f"/queries/{editor_query_id}"
        )
        response = self.api_client.call_api(method="DELETE", url=url)
        return AsyncRequestResponse.from_dict(response.json())

    def update_specified_query_metadata(
        self, severity: str, session_id: str, editor_query_id: str
    ) -> AsyncRequestResponse:
        """
        Args:
            severity (str):
            session_id (str):
            editor_query_id (str):

        Returns:
            AsyncRequestResponse
        """
        url = (
            f"{self.base_url}/sessions/{session_id}"
            f"/queries/{editor_query_id}/metadata"
        )
        response = self.api_client.call_api(
            method="PUT", url=url, json={"severity": severity}
        )
        return AsyncRequestResponse.from_dict(response.json())

    def update_multiple_query_sources(
        self, data: List[AuditQuery], session_id: str
    ) -> AsyncRequestResponse:
        url = f"{self.base_url}/sessions/{session_id}/queries/source"
        response = self.api_client.call_api(
            method="PUT",
            url=url,
            json=[asdict(item) for item in data],
        )
        return AsyncRequestResponse.from_dict(response.json())

    def validate_the_queries_provided(
        self, data: List[AuditQuery], session_id: str
    ) -> AsyncRequestResponse:
        url = f"{self.base_url}/sessions/{session_id}/queries/validate"
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json=[asdict(item) for item in data],
        )
        return AsyncRequestResponse.from_dict(response.json())

    def execute_the_queries_on_the_audit_session_scanned_project(
        self, data: List[AuditQuery], session_id: str
    ) -> AsyncRequestResponse:
        url = f"{self.base_url}/sessions/{session_id}/queries/run"
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json=[asdict(item) for item in data],
        )
        return AsyncRequestResponse.from_dict(response.json())

    def check_the_status_of_a_specified_request(
        self, session_id: str, request_id: str = None
    ) -> RequestStatus:
        url = (
            f"{self.base_url}/sessions/{session_id}"
            f"/requests/{request_id}"
        )
        response = self.api_client.call_api(method="GET", url=url)
        return RequestStatus.from_dict(response.json())

    def cancel_the_specified_request_execution(
        self, session_id: str, request_id: str = None
    ) -> bool:
        url = (
            f"{self.base_url}/sessions/{session_id}"
            f"/requests/{request_id}/cancel"
        )
        response = self.api_client.call_api(method="PUT", url=url)
        return response.status_code == OK

    def get_all_results_data_summary_tree_for_all_the_session_runs(
        self,
        session_id: str,
        run_id: str = None,
        hide_empty: bool = False,
    ) -> List[ResultsSummaryTree]:
        """
        Args:
            session_id (str): The session ID.
            run_id (str): Filter results by the query execution run id.
            hide_empty (bool): If true, hide queries that have 0
                results.

        Returns:
            List[ResultsSummaryTree]
        """
        url = f"{self.base_url}/sessions/{session_id}/results"
        params = {"runId": run_id, "hideEmpty": hide_empty}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return [
            ResultsSummaryTree.from_dict(item)
            for item in (response.json() or [])
        ]

    def get_all_vulnerabilities_related_to_a_given_result(
        self,
        session_id: str,
        result_id: str,
        page_size: int = 1000,
        current_page: int = 1,
    ) -> ResultsResponse:
        """
        Args:
            session_id (str):
            result_id (str):
            page_size (int):
            current_page (int):

        Returns:
            ResultsResponse
        """
        url = (
            f"{self.base_url}/sessions/{session_id}"
            f"/results/{result_id}/vulnerabilities"
        )
        params = {"pageSize": page_size, "currentPage": current_page}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return ResultsResponse.from_dict(response.json())

    def get_specified_vulnerability_data_such_as_attack_vector(
        self,
        session_id: str,
        result_id: str,
        vulnerability_id: str,
    ) -> ResultResponse:
        url = (
            f"{self.base_url}/sessions/{session_id}"
            f"/results/{result_id}/vulnerabilities/{vulnerability_id}"
        )
        response = self.api_client.call_api(method="GET", url=url)
        return ResultResponse.from_dict(response.json())

    def get_specified_result_debug_messages(
        self,
        session_id: str,
        result_id: str,
        page_size: int = 1000,
        current_page: int = 1,
    ) -> DebugMessageResponse:
        url = (
            f"{self.base_url}/sessions/{session_id}"
            f"/results/{result_id}/debug-messages"
        )
        params = {"pageSize": page_size, "currentPage": current_page}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return DebugMessageResponse.from_dict(response.json())

    def get_query_builder_history(
        self, session_id: str
    ) -> List[QueryBuilderMessage]:
        """
        Args:
            session_id (str):

        Returns:
            List[QueryBuilderMessage]
        """
        url = f"{self.base_url}/sessions/{session_id}/gpt"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            QueryBuilderMessage.from_dict(item)
            for item in (response.json() or [])
        ]

    def delete_query_builder_gpt_history(
        self, session_id: str
    ) -> bool:
        """
        Args:
            session_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/sessions/{session_id}/gpt"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def process_query_builder_gpt_request(
        self, data: QueryBuilderPrompt, session_id: str
    ) -> List[QueryBuilderMessage]:
        url = f"{self.base_url}/sessions/{session_id}/gpt"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(data)
        )
        return [
            QueryBuilderMessage.from_dict(item)
            for item in (response.json() or [])
        ]


def create_new_audit_session(data: SessionRequest) -> SessionResponse:
    return QueryEditorAPI().create_new_audit_session(data=data)


def heath_check_to_ensure_audit_session_is_kept_alive(
    session_id: str,
) -> bool:
    return QueryEditorAPI().heath_check_to_ensure_audit_session_is_kept_alive(
        session_id=session_id
    )


def delete_audit_session_with_specific_id(session_id: str) -> bool:
    return QueryEditorAPI().delete_audit_session_with_specific_id(
        session_id=session_id
    )


def get_the_logs_associated_to_the_audit_session(
    session_id: str,
) -> bytes:
    return QueryEditorAPI().get_the_logs_associated_to_the_audit_session(
        session_id=session_id
    )


def scan_the_audit_session_sources(
    session_id: str,
) -> AsyncRequestResponse:
    return QueryEditorAPI().scan_the_audit_session_sources(
        session_id=session_id
    )


def create_or_override_query(
    data: QueryRequest, session_id: str
) -> AsyncRequestResponse:
    return QueryEditorAPI().create_or_override_query(
        data=data, session_id=session_id
    )


def get_all_queries(
    session_id: str,
    level: str = None,
    ids: List[str] = None,
    filters: List[str] = None,
) -> List[QueriesTree]:
    return QueryEditorAPI().get_all_queries(
        session_id=session_id, level=level, ids=ids, filters=filters
    )


def get_data_of_a_specified_query(
    session_id: str,
    editor_query_id: str,
    include_metadata: bool = False,
    include_source: bool = False,
) -> QueryResponse:
    return QueryEditorAPI().get_data_of_a_specified_query(
        session_id=session_id,
        editor_query_id=editor_query_id,
        include_metadata=include_metadata,
        include_source=include_source,
    )


def delete_a_specified_custom_or_overridden_query(
    session_id: str, editor_query_id: str
) -> AsyncRequestResponse:
    return QueryEditorAPI().delete_a_specified_custom_or_overridden_query(
        session_id=session_id, editor_query_id=editor_query_id
    )


def update_specified_query_metadata(
    severity: str, session_id: str, editor_query_id: str
) -> AsyncRequestResponse:
    return QueryEditorAPI().update_specified_query_metadata(
        severity=severity,
        session_id=session_id,
        editor_query_id=editor_query_id,
    )


def update_multiple_query_sources(
    data: List[AuditQuery], session_id: str
) -> AsyncRequestResponse:
    return QueryEditorAPI().update_multiple_query_sources(
        data=data, session_id=session_id
    )


def validate_the_queries_provided(
    data: List[AuditQuery], session_id: str
) -> AsyncRequestResponse:
    return QueryEditorAPI().validate_the_queries_provided(
        data=data, session_id=session_id
    )


def execute_the_queries_on_the_audit_session_scanned_project(
    data: List[AuditQuery], session_id: str
) -> AsyncRequestResponse:
    return (
        QueryEditorAPI()
        .execute_the_queries_on_the_audit_session_scanned_project(
            data=data, session_id=session_id
        )
    )


def check_the_status_of_a_specified_request(
    session_id: str,
    request_id: str,
) -> RequestStatus:
    return QueryEditorAPI().check_the_status_of_a_specified_request(
        session_id=session_id, request_id=request_id
    )


def cancel_the_specified_request_execution(
    session_id: str,
    request_id: str,
) -> bool:
    return QueryEditorAPI().cancel_the_specified_request_execution(
        session_id=session_id, request_id=request_id
    )


def get_all_results_data_summary_tree_for_all_the_session_runs(
    session_id: str,
    run_id: str,
    hide_empty: bool = False,
) -> List[ResultsSummaryTree]:
    return QueryEditorAPI().get_all_results_data_summary_tree_for_all_the_session_runs(
        session_id=session_id, run_id=run_id, hide_empty=hide_empty
    )


def get_all_vulnerabilities_related_to_a_given_result(
    session_id: str,
    result_id: str,
    page_size: int = 1000,
    current_page: int = 1,
) -> ResultsResponse:
    return QueryEditorAPI().get_all_vulnerabilities_related_to_a_given_result(
        session_id=session_id,
        result_id=result_id,
        page_size=page_size,
        current_page=current_page,
    )


def get_specified_vulnerability_data_such_as_attack_vector(
    session_id: str, result_id: str, vulnerability_id: str
) -> ResultResponse:
    return QueryEditorAPI().get_specified_vulnerability_data_such_as_attack_vector(
        session_id=session_id,
        result_id=result_id,
        vulnerability_id=vulnerability_id,
    )


def get_specified_result_debug_messages(
    session_id: str,
    result_id: str,
    page_size: int = 1000,
    current_page: int = 1,
) -> DebugMessageResponse:
    return QueryEditorAPI().get_specified_result_debug_messages(
        session_id=session_id,
        result_id=result_id,
        page_size=page_size,
        current_page=current_page,
    )


def get_query_builder_history(
    session_id: str,
) -> List[QueryBuilderMessage]:
    return QueryEditorAPI().get_query_builder_history(session_id=session_id)


def delete_query_builder_gpt_history(session_id: str) -> bool:
    return QueryEditorAPI().delete_query_builder_gpt_history(
        session_id=session_id
    )


def process_query_builder_gpt_request(
    data: QueryBuilderPrompt, session_id: str
) -> List[QueryBuilderMessage]:
    return QueryEditorAPI().process_query_builder_gpt_request(
        data=data, session_id=session_id
    )
