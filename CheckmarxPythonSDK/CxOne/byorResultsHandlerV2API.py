# encoding: utf-8
from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, OK
from typing import List
from .dto import (
    ImportRequest,
    ImportResults,
    ByorJob,
    ByorJobPatchRequest,
)


class ByorResultsHandlerV2API(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/v2/byor"
        )

    def create_byor_import(self, import_request: ImportRequest) -> ImportResults:
        """
        Args:
            import_request (ImportRequest):

        Returns:
            ImportResults
        """
        url = f"{self.base_url}/imports"
        response = self.api_client.call_api(
            method="POST", url=url, json=asdict(import_request)
        )
        return ImportResults.from_dict(response.json())

    def get_job_by_id(self, job_id: str) -> ByorJob:
        """
        Args:
            job_id (str):

        Returns:
            ByorJob
        """
        url = f"{self.base_url}/jobs/{job_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return ByorJob.from_dict(response.json())

    def patch_job_by_id(
        self,
        job_id: str,
        patch_request: ByorJobPatchRequest = ByorJobPatchRequest(status="Canceled"),
    ) -> bool:
        """
        Args:
            job_id (str):
            patch_request (ByorJobPatchRequest):

        Returns:
            bool
        """
        url = f"{self.base_url}/jobs/{job_id}"
        response = self.api_client.call_api(
            method="PATCH", url=url, json=asdict(patch_request)
        )
        return response.status_code == NO_CONTENT

    def delete_import(self, import_id: str) -> bool:
        """
        Delete an import.

        Args:
            import_id (str):

        Returns:
            bool
        """
        url = f"{self.base_url}/imports/{import_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def get_aggregate_results(
        self,
        import_id: str,
        group_by_field: str,
        state: List[str] = None,
        status: List[str] = None,
        severity: List[str] = None,
        days_open: List[str] = None,
        search: str = None,
    ) -> dict:
        """
        Get aggregated results for an import.

        Args:
            import_id (str): ID of the import
            group_by_field (str): state, status, or severity
            state (List[str]): Filter by result state
            status (List[str]): Filter by result statuses
            severity (List[str]): Filter by result severities
            days_open (List[str]): Filter by days-open range (0-30, 31-60, 61-90, 90-)
            search (str): Search term

        Returns:
            dict
        """
        url = f"{self.base_url}/aggregate"
        params = {
            "import-id": import_id,
            "group-by-field": group_by_field,
            "state": state,
            "status": status,
            "severity": severity,
            "days-open": days_open,
            "search": search,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_a_list_of_imports(
        self,
        offset: int = 0,
        limit: int = 10,
        sort: str = None,
        from_date: str = None,
        to_date: str = None,
        file_type: str = None,
        search: str = None,
        status: List[str] = None,
        engine: str = None,
        import_id: List[str] = None,
        project_id: List[str] = None,
    ) -> dict:
        """
        Get a list of imports with filtering and pagination.

        Args:
            offset (int): Pagination offset. Default: 0
            limit (int): Items to return. Default: 10
            sort (str): +created_at or -created_at
            from_date (str): Start date (YYYY-MM-DD)
            to_date (str): End date (YYYY-MM-DD)
            file_type (str): Import file type (sarif)
            search (str): Search by project name
            status (List[str]): Filter by import statuses
            engine (str): Filter by engine
            import_id (List[str]): Filter by import IDs
            project_id (List[str]): Filter by project IDs

        Returns:
            dict
        """
        url = f"{self.base_url}/imports"
        params = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "from-date": from_date,
            "to-date": to_date,
            "file-type": file_type,
            "search": search,
            "status": status,
            "engine": engine,
            "import-id": import_id,
            "project-id": project_id,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_latest_imports(
        self, project_ids: List[str], status: List[str] = None
    ) -> dict:
        """
        Get the last import for each of the specified project IDs.

        Args:
            project_ids (List[str]): Comma-separated project UUIDs
            status (List[str]): Filter by import statuses

        Returns:
            dict mapping project-id to latestImport
        """
        url = f"{self.base_url}/imports/latest"
        params = {"project-ids": project_ids, "status": status}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_imports_summaries(
        self,
        import_ids: List[str],
        severity: List[str] = None,
        state: List[str] = None,
        status: List[str] = None,
    ) -> dict:
        """
        Get summaries for imports.

        Args:
            import_ids (List[str]): Import IDs
            severity (List[str]): Filter by severities
            state (List[str]): Filter by result state
            status (List[str]): Filter by result statuses

        Returns:
            dict
        """
        url = f"{self.base_url}/imports/summaries"
        params = {
            "import-ids": import_ids,
            "severity": severity,
            "state": state,
            "status": status,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_import_results(
        self,
        import_id: str,
        result_id: List[str] = None,
        state: List[str] = None,
        status: List[str] = None,
        severity: List[str] = None,
        days_open: List[str] = None,
        search: str = None,
        sort: str = None,
    ) -> dict:
        """
        Get results for a specific import.

        Args:
            import_id (str): ID of the import
            result_id (List[str]): Filter by result IDs
            state (List[str]): Filter by state
            status (List[str]): Filter by statuses
            severity (List[str]): Filter by severities
            days_open (List[str]): Filter by days-open range
            search (str): Search by vulnerability name
            sort (str): Sort order

        Returns:
            dict
        """
        url = f"{self.base_url}/imports/{import_id}/results"
        params = {
            "result-id": result_id,
            "state": state,
            "status": status,
            "severity": severity,
            "days-open": days_open,
            "search": search,
            "sort": sort,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def bulk_triage_import_results(
        self,
        import_id: str,
        project_id: str,
        result_ids: List[str],
        state: str = None,
        severity: str = None,
    ) -> bool:
        """
        Bulk triage results for an import.

        Args:
            import_id (str): ID of the import
            project_id (str): Project ID
            result_ids (List[str]): Result IDs to triage (max 1000)
            state (str): New state (optional)
            severity (str): New severity (optional)

        Returns:
            bool
        """
        url = f"{self.base_url}/imports/{import_id}/results/triages"
        body = {
            "projectId": project_id,
            "resultIds": result_ids,
            "state": state,
            "severity": severity,
        }
        response = self.api_client.call_api(
            method="PUT", url=url, json=body
        )
        return response.status_code == NO_CONTENT


def create_byor_import(import_request) -> ImportResults:
    return ByorResultsHandlerV2API().create_byor_import(import_request)


def get_job_by_id(job_id: str) -> ByorJob:
    return ByorResultsHandlerV2API().get_job_by_id(job_id=job_id)


def patch_job_by_id(job_id: str, patch_request: ByorJobPatchRequest) -> bool:
    return ByorResultsHandlerV2API().patch_job_by_id(
        job_id=job_id, patch_request=patch_request
    )


def delete_import(import_id: str) -> bool:
    return ByorResultsHandlerV2API().delete_import(import_id=import_id)


def get_aggregate_results(
    import_id: str,
    group_by_field: str,
    state: List[str] = None,
    status: List[str] = None,
    severity: List[str] = None,
    days_open: List[str] = None,
    search: str = None,
) -> dict:
    return ByorResultsHandlerV2API().get_aggregate_results(
        import_id=import_id,
        group_by_field=group_by_field,
        state=state,
        status=status,
        severity=severity,
        days_open=days_open,
        search=search,
    )


def get_a_list_of_imports(
    offset: int = 0,
    limit: int = 10,
    sort: str = None,
    from_date: str = None,
    to_date: str = None,
    file_type: str = None,
    search: str = None,
    status: List[str] = None,
    engine: str = None,
    import_id: List[str] = None,
    project_id: List[str] = None,
) -> dict:
    return ByorResultsHandlerV2API().get_a_list_of_imports(
        offset=offset,
        limit=limit,
        sort=sort,
        from_date=from_date,
        to_date=to_date,
        file_type=file_type,
        search=search,
        status=status,
        engine=engine,
        import_id=import_id,
        project_id=project_id,
    )


def get_latest_imports(
    project_ids: List[str], status: List[str] = None
) -> dict:
    return ByorResultsHandlerV2API().get_latest_imports(
        project_ids=project_ids, status=status
    )


def get_imports_summaries(
    import_ids: List[str],
    severity: List[str] = None,
    state: List[str] = None,
    status: List[str] = None,
) -> dict:
    return ByorResultsHandlerV2API().get_imports_summaries(
        import_ids=import_ids,
        severity=severity,
        state=state,
        status=status,
    )


def get_import_results(
    import_id: str,
    result_id: List[str] = None,
    state: List[str] = None,
    status: List[str] = None,
    severity: List[str] = None,
    days_open: List[str] = None,
    search: str = None,
    sort: str = None,
) -> dict:
    return ByorResultsHandlerV2API().get_import_results(
        import_id=import_id,
        result_id=result_id,
        state=state,
        status=status,
        severity=severity,
        days_open=days_open,
        search=search,
        sort=sort,
    )


def bulk_triage_import_results(
    import_id: str,
    project_id: str,
    result_ids: List[str],
    state: str = None,
    severity: str = None,
) -> bool:
    return ByorResultsHandlerV2API().bulk_triage_import_results(
        import_id=import_id,
        project_id=project_id,
        result_ids=result_ids,
        state=state,
        severity=severity,
    )
