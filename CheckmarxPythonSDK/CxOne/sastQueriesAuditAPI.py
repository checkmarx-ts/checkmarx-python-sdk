from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import (
    Queries,
    Query,
    QuerySearch,
    MethodInfo,
    QueryRequest,
    WorkspaceQuery,
    SessionRequest,
    SessionResponse,
    Sessions,
    Session,
    SastStatus,
    AuditQuery,
    GPTMessage,
)

from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, OK


class SastQueriesAuditAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/cx-audit"
        )

    def get_all_queries(self, project_id: str = None) -> List[Queries]:
        """
        Args:
            project_id (str):

        Returns:
            List[Queries]
        """
        url = f"{self.base_url}/queries"
        params = {"projectId": project_id}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return [Queries.from_dict(item) for item in (response.json() or [])]

    def create_new_query(
        self, session_id: str, data: QueryRequest
    ) -> bool:
        """
        Args:
            session_id (str):
            data (QueryRequest):

        Returns:
            bool
        """
        url = f"{self.base_url}/query-editor/sessions/{session_id}/queries"
        response = self.api_client.call_api(
            method="POST", url=url,
            json={k: v for k, v in asdict(data).items() if v is not None}
        )
        return response.status_code == OK

    def get_all_queries_search(self, session_id: str) -> List[QuerySearch]:
        """
        Args:
            session_id (str):

        Returns:
            List[QuerySearch]
        """
        url = f"{self.base_url}/queries/{session_id}/search"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            QuerySearch.from_dict(item) for item in (response.json() or [])
        ]

    def get_queries_metadata(self) -> List[MethodInfo]:
        """
        Returns:
            List[MethodInfo]
        """
        url = f"{self.base_url}/queries/metadata"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            MethodInfo.from_dict(item) for item in (response.json() or [])
        ]

    def get_query_source(self, level: str, path: str) -> Query:
        """
        Args:
            level (str):
            path (str):

        Returns:
            Query
        """
        url = f"{self.base_url}/queries/{level}/{path}"
        response = self.api_client.call_api(method="GET", url=url)
        return Query.from_dict(response.json())

    def delete_overridden_query(self, level: str, path: str) -> bool:
        """
        Args:
            level (str):
            path (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/queries/{level}/{path}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def update_query_source(
        self, data: List[WorkspaceQuery], session_id: str, level: str
    ) -> bool:
        """
        Args:
            data (List[WorkspaceQuery]):
            session_id (str):
            level (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/queries/{session_id}/{level}"
        response = self.api_client.call_api(
            method="PUT",
            url=url,
            json=[asdict(query) for query in data],
        )
        return response.status_code == OK

    def create_new_session(self, data: SessionRequest) -> SessionResponse:
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

    def get_all_active_sessions_related_to_web_audit(
        self, project_id: str = None, scan_id: str = None
    ) -> Sessions:
        """
        Args:
            project_id (str):
            scan_id (str):

        Returns:
            Sessions
        """
        url = f"{self.base_url}/sessions"
        params = {"projectId": project_id, "scanId": scan_id}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return Sessions.from_dict(response.json())

    def get_session_details(self, session_id: str) -> Session:
        """
        Args:
            session_id (str):

        Returns:
            Session
        """
        url = f"{self.base_url}/sessions/{session_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return Session.from_dict(response.json())

    def delete_session_with_specific_id(self, session_id: str) -> bool:
        """
        Args:
            session_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/sessions/{session_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def health_check_to_ensure_session_is_kept_alive(
        self, session_id: str
    ) -> bool:
        """
        Args:
            session_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/sessions/{session_id}"
        response = self.api_client.call_api(method="POST", url=url)
        return response.status_code == NO_CONTENT

    def check_if_sast_engine_is_ready_to_use(
        self, session_id: str
    ) -> SastStatus:
        """
        Args:
            session_id (str):

        Returns:
            SastStatus
        """
        url = f"{self.base_url}/sessions/{session_id}/sast-status"
        response = self.api_client.call_api(method="GET", url=url)
        return SastStatus.from_dict(response.json())

    def check_the_status_of_some_scan_related_requests(
        self, session_id: str, status_type: int
    ) -> dict:
        """
        Args:
            session_id (str):
            status_type (int):

        Returns:
            dict
        """
        url = f"{self.base_url}/sessions/{session_id}/request-status"
        params = {"type": status_type}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def detect_the_languages_of_the_project_to_scan(
        self, session_id: str
    ) -> int:
        """
        Args:
            session_id (str):

        Returns:
            int
        """
        url = f"{self.base_url}/sessions/{session_id}/project/languages"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def scan_the_project_using_sast_engine(self, session_id: str) -> int:
        """
        Args:
            session_id (str):

        Returns:
            int
        """
        url = f"{self.base_url}/sessions/{session_id}/project/scan"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def compile_the_queries_of_the_scanned_project(
        self, data: List[AuditQuery], session_id: str
    ) -> int:
        """
        Args:
            data (List[AuditQuery]):
            session_id (str):

        Returns:
            int
        """
        url = f"{self.base_url}/sessions/{session_id}/queries/compile"
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json=[asdict(query) for query in data],
        )
        return response.json()

    def execute_the_queries_of_the_scanned_project(
        self, data: List[AuditQuery], session_id: str
    ) -> int:
        """
        Args:
            data (List[AuditQuery]):
            session_id (str):

        Returns:
            int
        """
        url = f"{self.base_url}/sessions/{session_id}/queries/run"
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json=[asdict(query) for query in data],
        )
        return response.json()

    def cancel_the_queries_execution(self, session_id: str) -> bool:
        """
        Args:
            session_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/sessions/{session_id}/queries/cancel"
        response = self.api_client.call_api(method="GET", url=url)
        return response.status_code == OK

    def get_the_logs_associated_to_the_audit_session(
        self, session_id: str
    ) -> str:
        """
        Args:
            session_id (str):

        Returns:
            str
        """
        url = f"{self.base_url}/sessions/{session_id}/logs"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def retrieve_gpt_history(self, session_id: str) -> List[GPTMessage]:
        """
        Args:
            session_id (str):

        Returns:
            List[GPTMessage]
        """
        url = f"{self.base_url}/gpt/{session_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            GPTMessage.from_dict(item) for item in (response.json() or [])
        ]

    def delete_gpt_history(self, session_id: str) -> bool:
        """
        Args:
            session_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/gpt/{session_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def process_gpt_prompt_request(
        self, data: dict, session_id: str
    ) -> List[GPTMessage]:
        """
        Args:
            data (dict):
            session_id (str):

        Returns:
            List[GPTMessage]
        """
        url = f"{self.base_url}/gpt/{session_id}"
        response = self.api_client.call_api(
            method="POST", url=url, json=data
        )
        return [
            GPTMessage.from_dict(item) for item in (response.json() or [])
        ]


def get_all_queries(project_id: str = None) -> List[Queries]:
    return SastQueriesAuditAPI().get_all_queries(project_id=project_id)


def create_new_query(session_id: str, data: QueryRequest) -> bool:
    return SastQueriesAuditAPI().create_new_query(
        session_id=session_id, data=data
    )


def get_all_queries_search(session_id: str) -> List[QuerySearch]:
    return SastQueriesAuditAPI().get_all_queries_search(
        session_id=session_id
    )


def get_queries_metadata() -> List[MethodInfo]:
    return SastQueriesAuditAPI().get_queries_metadata()


def get_query_source(level: str, path: str) -> Query:
    return SastQueriesAuditAPI().get_query_source(level=level, path=path)


def delete_overridden_query(level: str, path: str) -> bool:
    return SastQueriesAuditAPI().delete_overridden_query(
        level=level, path=path
    )


def update_query_source(
    data: List[WorkspaceQuery], session_id: str, level: str
) -> bool:
    return SastQueriesAuditAPI().update_query_source(
        data=data, session_id=session_id, level=level
    )


def create_new_session(data: SessionRequest) -> SessionResponse:
    return SastQueriesAuditAPI().create_new_session(data=data)


def get_all_active_sessions_related_to_web_audit(
    project_id: str = None, scan_id: str = None
) -> Sessions:
    return SastQueriesAuditAPI().get_all_active_sessions_related_to_web_audit(
        project_id=project_id, scan_id=scan_id
    )


def get_session_details(session_id: str) -> Session:
    return SastQueriesAuditAPI().get_session_details(session_id=session_id)


def delete_session_with_specific_id(session_id: str) -> bool:
    return SastQueriesAuditAPI().delete_session_with_specific_id(
        session_id=session_id
    )


def health_check_to_ensure_session_is_kept_alive(session_id: str) -> bool:
    return SastQueriesAuditAPI().health_check_to_ensure_session_is_kept_alive(
        session_id=session_id
    )


def check_if_sast_engine_is_ready_to_use(session_id: str) -> SastStatus:
    return SastQueriesAuditAPI().check_if_sast_engine_is_ready_to_use(
        session_id=session_id
    )


def check_the_status_of_some_scan_related_requests(
    session_id: str, status_type: int
):
    return SastQueriesAuditAPI().check_the_status_of_some_scan_related_requests(
        session_id=session_id, status_type=status_type
    )


def detect_the_languages_of_the_project_to_scan(session_id: str) -> int:
    return SastQueriesAuditAPI().detect_the_languages_of_the_project_to_scan(
        session_id=session_id
    )


def scan_the_project_using_sast_engine(session_id: str) -> int:
    return SastQueriesAuditAPI().scan_the_project_using_sast_engine(
        session_id=session_id
    )


def compile_the_queries_of_the_scanned_project(
    data: List[AuditQuery], session_id: str
) -> int:
    return SastQueriesAuditAPI().compile_the_queries_of_the_scanned_project(
        data=data, session_id=session_id
    )


def execute_the_queries_of_the_scanned_project(
    data: List[AuditQuery], session_id: str
) -> int:
    return SastQueriesAuditAPI().execute_the_queries_of_the_scanned_project(
        data=data, session_id=session_id
    )


def cancel_the_queries_execution(session_id: str) -> bool:
    return SastQueriesAuditAPI().cancel_the_queries_execution(
        session_id=session_id
    )


def get_the_logs_associated_to_the_audit_session(session_id: str) -> str:
    return SastQueriesAuditAPI().get_the_logs_associated_to_the_audit_session(
        session_id=session_id
    )


def retrieve_gpt_history(session_id: str) -> List[GPTMessage]:
    return SastQueriesAuditAPI().retrieve_gpt_history(session_id=session_id)


def delete_gpt_history(session_id: str) -> bool:
    return SastQueriesAuditAPI().delete_gpt_history(session_id=session_id)


def process_gpt_prompt_request(
    data: dict, session_id: str
) -> List[GPTMessage]:
    return SastQueriesAuditAPI().process_gpt_prompt_request(
        data=data, session_id=session_id
    )
