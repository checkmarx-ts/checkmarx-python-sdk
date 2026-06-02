from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class MicroEnginesAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/micro-engines"
        )

    # ---- SSCS.yaml: Write-side (6 GET) ----

    def get_predicates_history(
        self, similarity_id: str, project_ids: List[str] = None
    ) -> dict:
        """
        Get predicates history by similarity ID.

        Args:
            similarity_id (str):
            project_ids (List[str]): Project IDs to filter by

        Returns:
            dict with predicates, projectId, similarityId, totalCount
        """
        url = f"{self.base_url}/predicates/{similarity_id}"
        params = {"project-ids": project_ids}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_projects(
        self,
        page_size: int = None,
        current_page: int = None,
        filters: str = None,
        sort: str = None,
        search: str = None,
    ) -> dict:
        """
        Get list of micro-engine projects.

        Args:
            page_size (int):
            current_page (int):
            filters (str): Filter expression
            sort (str): Sort expression
            search (str): Search term

        Returns:
            dict with entries, totalCount, totalFilteredCount
        """
        url = f"{self.base_url}/projects"
        params = {
            "pageSize": page_size,
            "currentPage": current_page,
            "filters": filters,
            "sort": sort,
            "search": search,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_project(self, project: str, scan: str = None) -> dict:
        """
        Get a single micro-engine project.

        Args:
            project (str): Project ID
            scan (str): Optional scan ID

        Returns:
            dict with engines, name, id, riskLevel, etc.
        """
        url = f"{self.base_url}/projects/{project}"
        params = {"scan": scan}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_engine_results(
        self,
        project: str,
        scan: str,
        engine: str,
        filters: str = None,
        page_size: int = None,
        current_page: int = None,
        sort: str = None,
        search: str = None,
    ) -> dict:
        """
        Get engine results by project, scan, and engine.

        Args:
            project (str): Project ID
            scan (str): Scan ID
            engine (str): Engine name (e.g. '2ms', 'Scorecard')
            filters (str): Filter expression
            page_size (int):
            current_page (int):
            sort (str): Sort expression
            search (str): Search term

        Returns:
            dict with entries, totalCount
        """
        url = f"{self.base_url}/results/{project}/{scan}/{engine}"
        params = {
            "filters": filters,
            "pageSize": page_size,
            "currentPage": current_page,
            "sort": sort,
            "search": search,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_result_groups(
        self,
        project: str,
        scan: str,
        engine: str,
        column: str,
        search: str = None,
        filters: str = None,
    ) -> dict:
        """
        Get grouped results by column.

        Args:
            project (str): Project ID
            scan (str): Scan ID
            engine (str): Engine name
            column (str): Column to group by
            search (str): Search term
            filters (str): Filter expression

        Returns:
            dict with entries (list of Group)
        """
        url = (
            f"{self.base_url}/results/{project}/{scan}/{engine}"
            f"/groups/{column}"
        )
        params = {"search": search, "filters": filters}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_scan_overview(self, scan: str) -> dict:
        """
        Get scan overview for a micro-engine scan.

        Args:
            scan (str): Scan ID

        Returns:
            dict with engineOverviews, id, projectId, riskSummary, status, totalRisks
        """
        url = f"{self.base_url}/scans/{scan}/scan-overview"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    # ---- SSCS_READER.yaml: Read-side (6 GET) ----

    def read_predicates_history(
        self, similarity_id: str, project_ids: List[str] = None
    ) -> dict:
        """
        Read predicates history by similarity ID (read-optimized).

        Args:
            similarity_id (str):
            project_ids (List[str]): Project IDs to filter by

        Returns:
            dict with predicateHistoryPerProject, totalCount
        """
        url = f"{self.base_url}/read/predicates/{similarity_id}"
        params = {"project-ids": project_ids}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def read_projects(
        self,
        page_size: int = None,
        current_page: int = None,
        filters: str = None,
        sort: str = None,
        search: str = None,
    ) -> dict:
        """
        Read micro-engine projects (read-optimized).

        Args:
            page_size (int):
            current_page (int):
            filters (str): Filter expression
            sort (str): Sort expression
            search (str): Search term

        Returns:
            dict with entries, totalCount, totalFilteredCount
        """
        url = f"{self.base_url}/read/projects"
        params = {
            "pageSize": page_size,
            "currentPage": current_page,
            "filters": filters,
            "sort": sort,
            "search": search,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def read_project(self, project: str, scan: str = None) -> dict:
        """
        Read a single micro-engine project (read-optimized).

        Args:
            project (str): Project ID
            scan (str): Optional scan ID

        Returns:
            dict with engines, name, id, riskLevel, etc.
        """
        url = f"{self.base_url}/read/projects/{project}"
        params = {"scan": scan}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def read_engine_results(
        self,
        project: str,
        scan: str,
        engine: str,
        filters: str = None,
        page_size: int = None,
        current_page: int = None,
        sort: str = None,
        search: str = None,
    ) -> dict:
        """
        Read engine results (read-optimized, includes similarityId, state, status).

        Args:
            project (str): Project ID
            scan (str): Scan ID
            engine (str): Engine name
            filters (str): Filter expression
            page_size (int):
            current_page (int):
            sort (str): Sort expression
            search (str): Search term

        Returns:
            dict with entries, totalCount
        """
        url = f"{self.base_url}/read/results/{project}/{scan}/{engine}"
        params = {
            "filters": filters,
            "pageSize": page_size,
            "currentPage": current_page,
            "sort": sort,
            "search": search,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def read_result_groups(
        self,
        project: str,
        scan: str,
        engine: str,
        column: str,
        search: str = None,
        filters: str = None,
    ) -> dict:
        """
        Read grouped results (read-optimized).

        Args:
            project (str): Project ID
            scan (str): Scan ID
            engine (str): Engine name
            column (str): Column to group by
            search (str): Search term
            filters (str): Filter expression

        Returns:
            dict with entries
        """
        url = (
            f"{self.base_url}/read/results/{project}/{scan}/{engine}"
            f"/groups/{column}"
        )
        params = {"search": search, "filters": filters}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def read_scan_overview(self, scan: str) -> dict:
        """
        Read scan overview (read-optimized).

        Args:
            scan (str): Scan ID

        Returns:
            dict with engineOverviews, id, projectId, riskSummary, status, totalRisks
        """
        url = f"{self.base_url}/read/scans/{scan}/scan-overview"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    # ---- SSCS_CORRELATOR.yaml: Write-side (1 POST) ----

    def post_predicates(self, data: List[dict]) -> str:
        """
        Write/bulk-update predicates (correlator).

        Args:
            data (List[dict]): Array of BasePredicate objects, each with
                projectId (required), severity (required),
                similarityId (required), state (required),
                comment (optional, max 1024), microengine (optional),
                scanId (optional)

        Returns:
            str response from the API
        """
        url = f"{self.base_url}/write/predicates"
        response = self.api_client.call_api(
            method="POST", url=url, json=data
        )
        return response.text


# ---- Module-level convenience functions ----

def get_predicates_history(
    similarity_id: str, project_ids: List[str] = None
) -> dict:
    return MicroEnginesAPI().get_predicates_history(
        similarity_id=similarity_id, project_ids=project_ids
    )


def get_projects(
    page_size: int = None,
    current_page: int = None,
    filters: str = None,
    sort: str = None,
    search: str = None,
) -> dict:
    return MicroEnginesAPI().get_projects(
        page_size=page_size, current_page=current_page,
        filters=filters, sort=sort, search=search,
    )


def get_project(project: str, scan: str = None) -> dict:
    return MicroEnginesAPI().get_project(project=project, scan=scan)


def get_engine_results(
    project: str,
    scan: str,
    engine: str,
    filters: str = None,
    page_size: int = None,
    current_page: int = None,
    sort: str = None,
    search: str = None,
) -> dict:
    return MicroEnginesAPI().get_engine_results(
        project=project, scan=scan, engine=engine,
        filters=filters, page_size=page_size, current_page=current_page,
        sort=sort, search=search,
    )


def get_result_groups(
    project: str,
    scan: str,
    engine: str,
    column: str,
    search: str = None,
    filters: str = None,
) -> dict:
    return MicroEnginesAPI().get_result_groups(
        project=project, scan=scan, engine=engine, column=column,
        search=search, filters=filters,
    )


def get_scan_overview(scan: str) -> dict:
    return MicroEnginesAPI().get_scan_overview(scan=scan)


def read_predicates_history(
    similarity_id: str, project_ids: List[str] = None
) -> dict:
    return MicroEnginesAPI().read_predicates_history(
        similarity_id=similarity_id, project_ids=project_ids
    )


def read_projects(
    page_size: int = None,
    current_page: int = None,
    filters: str = None,
    sort: str = None,
    search: str = None,
) -> dict:
    return MicroEnginesAPI().read_projects(
        page_size=page_size, current_page=current_page,
        filters=filters, sort=sort, search=search,
    )


def read_project(project: str, scan: str = None) -> dict:
    return MicroEnginesAPI().read_project(project=project, scan=scan)


def read_engine_results(
    project: str,
    scan: str,
    engine: str,
    filters: str = None,
    page_size: int = None,
    current_page: int = None,
    sort: str = None,
    search: str = None,
) -> dict:
    return MicroEnginesAPI().read_engine_results(
        project=project, scan=scan, engine=engine,
        filters=filters, page_size=page_size, current_page=current_page,
        sort=sort, search=search,
    )


def read_result_groups(
    project: str,
    scan: str,
    engine: str,
    column: str,
    search: str = None,
    filters: str = None,
) -> dict:
    return MicroEnginesAPI().read_result_groups(
        project=project, scan=scan, engine=engine, column=column,
        search=search, filters=filters,
    )


def read_scan_overview(scan: str) -> dict:
    return MicroEnginesAPI().read_scan_overview(scan=scan)


def post_predicates(data: List[dict]) -> str:
    return MicroEnginesAPI().post_predicates(data=data)
