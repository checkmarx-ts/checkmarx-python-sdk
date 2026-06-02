from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class AiAssetsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/ai-sc"
        )

    def get_ai_findings(
        self,
        limit: int = None,
        offset: int = 0,
        project_ids: str = None,
        asset_names: str = None,
        providers: str = None,
        search: str = None,
        asset_type_ids: str = None,
        application_ids: str = None,
        order_column: str = None,
        order_direction: str = None,
        include_evidences: bool = False,
    ) -> dict:
        """
        Get a list of all findings for the tenant.

        Args:
            limit (int): Max results (1-100)
            offset (int): Items to skip. Default: 0
            project_ids (str): Comma-separated project UUIDs
            asset_names (str): Comma-separated asset names
            providers (str): Comma-separated providers
            search (str): Search term
            asset_type_ids (str): Comma-separated asset type UUIDs
            application_ids (str): Comma-separated application UUIDs
            order_column (str): created-at, updated-at, scan-date,
                project-name, asset-name
            order_direction (str): asc or desc
            include_evidences (bool): Include evidence details

        Returns:
            dict with data, total, currentPage, lastPage
        """
        url = f"{self.base_url}/findings"
        params = {
            "limit": limit,
            "offset": offset,
            "project-ids": project_ids,
            "asset-names": asset_names,
            "providers": providers,
            "search": search,
            "asset-type-ids": asset_type_ids,
            "application-ids": application_ids,
            "order-column": order_column,
            "order-direction": order_direction,
            "include-evidences": include_evidences,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_ai_findings_aggregate(
        self,
        group_by: str,
        limit: int = None,
        offset: int = 0,
        project_ids: str = None,
        asset_names: str = None,
        providers: str = None,
        search: str = None,
        asset_type_ids: str = None,
        application_ids: str = None,
    ) -> dict:
        """
        Aggregate findings grouped by specified fields.

        Args:
            group_by (str): assetType, projectName, or applicationName
            limit (int): Max results (1-100)
            offset (int): Items to skip. Default: 0
            project_ids (str): Comma-separated project UUIDs
            asset_names (str): Comma-separated asset names
            providers (str): Comma-separated providers
            search (str): Search term
            asset_type_ids (str): Comma-separated asset type UUIDs
            application_ids (str): Comma-separated application UUIDs

        Returns:
            dict with groupsCounter
        """
        url = f"{self.base_url}/findings/aggregate"
        params = {
            "group-by": group_by,
            "limit": limit,
            "offset": offset,
            "project-ids": project_ids,
            "asset-names": asset_names,
            "providers": providers,
            "search": search,
            "asset-type-ids": asset_type_ids,
            "application-ids": application_ids,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_ai_finding_by_id(self, id: str) -> dict:
        """
        Get a specific finding by ID.

        Args:
            id (str): Finding ID (uuid)

        Returns:
            dict with id, asset, project, evidences, etc.
        """
        url = f"{self.base_url}/finding/{id}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_asset_types(self) -> List[dict]:
        """
        Get a list of all asset types.

        Returns:
            list of dict with id, match_format, display_format, created_at
        """
        url = f"{self.base_url}/asset-types"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_assets(
        self, limit: int = None, offset: int = 0
    ) -> dict:
        """
        Get a list of all assets for the tenant.

        Args:
            limit (int): Max results (1-100)
            offset (int): Items to skip. Default: 0

        Returns:
            dict with data, total, currentPage, lastPage
        """
        url = f"{self.base_url}/assets"
        params = {"limit": limit, "offset": offset}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_applications(
        self, limit: int = None, offset: int = 0
    ) -> dict:
        """
        Get a list of all AI-scope applications for the tenant.

        Args:
            limit (int): Max results (1-100)
            offset (int): Items to skip. Default: 0

        Returns:
            dict with data, total, currentPage, lastPage
        """
        url = f"{self.base_url}/applications"
        params = {"limit": limit, "offset": offset}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    # ---- AI Supply Chain Global Inventory (same /api/ai-sc base) ----

    def get_global_inventory_results(
        self,
        limit: int = None,
        offset: int = 0,
        project_ids: str = None,
        asset_names: str = None,
        providers: str = None,
        search: str = None,
        asset_type_ids: str = None,
        application_ids: str = None,
        order_column: str = None,
        order_direction: str = None,
        include_evidences: bool = False,
    ) -> dict:
        """
        Get a list of all results for the tenant (global inventory).

        Args:
            limit (int): Max results (1-100)
            offset (int): Items to skip. Default: 0
            project_ids (str): Comma-separated project UUIDs
            asset_names (str): Comma-separated asset names
            providers (str): Comma-separated providers
            search (str): Search term
            asset_type_ids (str): Comma-separated asset type UUIDs
            application_ids (str): Comma-separated application UUIDs
            order_column (str): created-at, updated-at, scan-date,
                project-name, asset-name
            order_direction (str): asc, desc, ASC, DESC
            include_evidences (bool): Include evidence details

        Returns:
            dict with data, total, currentPage, lastPage
        """
        url = f"{self.base_url}/global-inventory/results"
        params = {
            "limit": limit,
            "offset": offset,
            "project-ids": project_ids,
            "asset-names": asset_names,
            "providers": providers,
            "search": search,
            "asset-type-ids": asset_type_ids,
            "application-ids": application_ids,
            "order-column": order_column,
            "order-direction": order_direction,
            "include-evidences": include_evidences,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_global_inventory_result_by_id(self, id: str) -> dict:
        """
        Get a specific global inventory result by ID.

        Args:
            id (str): Result ID (uuid)

        Returns:
            dict with id, asset, project, evidences, etc.
        """
        url = f"{self.base_url}/global-inventory/result/{id}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def aggregate_global_inventory_results(
        self,
        group_by: str,
        project_ids: str = None,
        asset_names: str = None,
        providers: str = None,
        search: str = None,
        asset_type_ids: str = None,
        application_ids: str = None,
    ) -> dict:
        """
        Aggregate global inventory results grouped by specified fields.

        Args:
            group_by (str): assetType, projectName, applicationName,
                assetName, or provider
            project_ids (str): Comma-separated project UUIDs
            asset_names (str): Comma-separated asset names
            providers (str): Comma-separated providers
            search (str): Search term
            asset_type_ids (str): Comma-separated asset type UUIDs
            application_ids (str): Comma-separated application UUIDs

        Returns:
            dict with groupsCounter
        """
        url = f"{self.base_url}/global-inventory/results/aggregate"
        params = {
            "group-by": group_by,
            "project-ids": project_ids,
            "asset-names": asset_names,
            "providers": providers,
            "search": search,
            "asset-type-ids": asset_type_ids,
            "application-ids": application_ids,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    # ---- AI Supply Chain Scan Results (/api/ai-sc/reader) ----

    def get_scan_results(
        self,
        scan_id: str,
        search: str = None,
        asset_type_ids: str = None,
        asset_names: str = None,
        providers: str = None,
        version: str = None,
        first_detection_date_time: str = None,
        state: List[str] = None,
        path: str = None,
        limit: int = None,
        offset: int = 1,
        order_column: str = None,
        order_direction: str = None,
    ) -> dict:
        """
        Get AI supply chain results for a specific scan.

        Args:
            scan_id (str): Scan ID (uuid)
            search (str): Full-text search
            asset_type_ids (str): Comma-separated asset type UUIDs
            asset_names (str): Comma-separated asset names
            providers (str): Comma-separated providers
            version (str): Filter by version
            first_detection_date_time (str): Filter by detection time (date-time)
            state (List[str]): Filter by state
            path (str): Filter by file location
            limit (int): Max results (1-100)
            offset (int): 1-based page number. Default: 1
            order_column (str): assetType, assetName, provider, version,
                firstDetectionDateTime, state. Default: assetName
            order_direction (str): asc, desc, ASC, DESC. Default: desc

        Returns:
            dict with data, total, currentPage, lastPage
        """
        url = f"{self.base_url}/reader/scans/{scan_id}/results"
        params = {
            "search": search,
            "asset-type-ids": asset_type_ids,
            "asset-names": asset_names,
            "providers": providers,
            "version": version,
            "firstDetectionDateTime": first_detection_date_time,
            "state": state,
            "path": path,
            "limit": limit,
            "offset": offset,
            "orderColumn": order_column,
            "orderDirection": order_direction,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def aggregate_scan_results(
        self,
        scan_id: str,
        group_by: str,
        search: str = None,
        asset_type_ids: str = None,
        asset_names: str = None,
        providers: str = None,
        version: str = None,
        first_detection_date_time: str = None,
        state: List[str] = None,
        path: str = None,
    ) -> dict:
        """
        Aggregate scan results groups by specified fields.

        Args:
            scan_id (str): Scan ID (uuid)
            group_by (str): 1-3 comma-separated fields:
                assetType, assetName, provider
            search (str): Full-text search
            asset_type_ids (str): Comma-separated asset type UUIDs
            asset_names (str): Comma-separated asset names
            providers (str): Comma-separated providers
            version (str): Filter by version
            first_detection_date_time (str): Filter by detection time
            state (List[str]): Filter by state
            path (str): Filter by file location

        Returns:
            dict with scanGroupsCounter
        """
        url = f"{self.base_url}/reader/scans/{scan_id}/results/aggregate"
        params = {
            "groupBy": group_by,
            "search": search,
            "asset-type-ids": asset_type_ids,
            "asset-names": asset_names,
            "providers": providers,
            "version": version,
            "firstDetectionDateTime": first_detection_date_time,
            "state": state,
            "path": path,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_asset_risks(
        self,
        scan_id: str,
        asset_id: str,
        severities: str = None,
        names: str = None,
        risk_ids: str = None,
        file_path: str = None,
        search: str = None,
        order_column: str = None,
        order_direction: str = None,
        limit: int = None,
        offset: int = 1,
    ) -> dict:
        """
        Get LLM-assessed risks for a specific asset in a scan.

        Args:
            scan_id (str): Scan ID (uuid)
            asset_id (str): Discovery asset ID
            severities (str): Comma-separated severity labels
            names (str): Comma-separated risk names (case-insensitive)
            risk_ids (str): Comma-separated risk IDs
            file_path (str): Substring match on file paths
            search (str): Full-text search
            order_column (str): name, severity, riskId
            order_direction (str): asc, desc
            limit (int): Max results (1-100)
            offset (int): 1-based page number. Default: 1

        Returns:
            dict with scanId, assetId, assetName, risks, riskCountBySeverity
        """
        url = (
            f"{self.base_url}/reader/scans/{scan_id}"
            f"/assets/{asset_id}/risks"
        )
        params = {
            "severities": severities,
            "names": names,
            "riskIds": risk_ids,
            "filePath": file_path,
            "search": search,
            "orderColumn": order_column,
            "orderDirection": order_direction,
            "limit": limit,
            "offset": offset,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()


# ---- Module-level convenience functions ----

def get_ai_findings(
    limit: int = None,
    offset: int = 0,
    project_ids: str = None,
    asset_names: str = None,
    providers: str = None,
    search: str = None,
    asset_type_ids: str = None,
    application_ids: str = None,
    order_column: str = None,
    order_direction: str = None,
    include_evidences: bool = False,
) -> dict:
    return AiAssetsAPI().get_ai_findings(
        limit=limit, offset=offset, project_ids=project_ids,
        asset_names=asset_names, providers=providers, search=search,
        asset_type_ids=asset_type_ids, application_ids=application_ids,
        order_column=order_column, order_direction=order_direction,
        include_evidences=include_evidences,
    )


def get_ai_findings_aggregate(
    group_by: str,
    limit: int = None,
    offset: int = 0,
    project_ids: str = None,
    asset_names: str = None,
    providers: str = None,
    search: str = None,
    asset_type_ids: str = None,
    application_ids: str = None,
) -> dict:
    return AiAssetsAPI().get_ai_findings_aggregate(
        group_by=group_by, limit=limit, offset=offset,
        project_ids=project_ids, asset_names=asset_names,
        providers=providers, search=search,
        asset_type_ids=asset_type_ids, application_ids=application_ids,
    )


def get_ai_finding_by_id(id: str) -> dict:
    return AiAssetsAPI().get_ai_finding_by_id(id=id)


def get_ai_asset_types() -> List[dict]:
    return AiAssetsAPI().get_asset_types()


def get_ai_assets(limit: int = None, offset: int = 0) -> dict:
    return AiAssetsAPI().get_assets(limit=limit, offset=offset)


def get_ai_applications(limit: int = None, offset: int = 0) -> dict:
    return AiAssetsAPI().get_applications(limit=limit, offset=offset)


def get_global_inventory_results(
    limit: int = None,
    offset: int = 0,
    project_ids: str = None,
    asset_names: str = None,
    providers: str = None,
    search: str = None,
    asset_type_ids: str = None,
    application_ids: str = None,
    order_column: str = None,
    order_direction: str = None,
    include_evidences: bool = False,
) -> dict:
    return AiAssetsAPI().get_global_inventory_results(
        limit=limit, offset=offset, project_ids=project_ids,
        asset_names=asset_names, providers=providers, search=search,
        asset_type_ids=asset_type_ids, application_ids=application_ids,
        order_column=order_column, order_direction=order_direction,
        include_evidences=include_evidences,
    )


def get_global_inventory_result_by_id(id: str) -> dict:
    return AiAssetsAPI().get_global_inventory_result_by_id(id=id)


def aggregate_global_inventory_results(
    group_by: str,
    project_ids: str = None,
    asset_names: str = None,
    providers: str = None,
    search: str = None,
    asset_type_ids: str = None,
    application_ids: str = None,
) -> dict:
    return AiAssetsAPI().aggregate_global_inventory_results(
        group_by=group_by, project_ids=project_ids, asset_names=asset_names,
        providers=providers, search=search, asset_type_ids=asset_type_ids,
        application_ids=application_ids,
    )


def get_scan_results(
    scan_id: str,
    search: str = None,
    asset_type_ids: str = None,
    asset_names: str = None,
    providers: str = None,
    version: str = None,
    first_detection_date_time: str = None,
    state: List[str] = None,
    path: str = None,
    limit: int = None,
    offset: int = 1,
    order_column: str = None,
    order_direction: str = None,
) -> dict:
    return AiAssetsAPI().get_scan_results(
        scan_id=scan_id, search=search, asset_type_ids=asset_type_ids,
        asset_names=asset_names, providers=providers, version=version,
        first_detection_date_time=first_detection_date_time, state=state,
        path=path, limit=limit, offset=offset, order_column=order_column,
        order_direction=order_direction,
    )


def aggregate_scan_results(
    scan_id: str,
    group_by: str,
    search: str = None,
    asset_type_ids: str = None,
    asset_names: str = None,
    providers: str = None,
    version: str = None,
    first_detection_date_time: str = None,
    state: List[str] = None,
    path: str = None,
) -> dict:
    return AiAssetsAPI().aggregate_scan_results(
        scan_id=scan_id, group_by=group_by, search=search,
        asset_type_ids=asset_type_ids, asset_names=asset_names,
        providers=providers, version=version,
        first_detection_date_time=first_detection_date_time,
        state=state, path=path,
    )


def get_asset_risks(
    scan_id: str,
    asset_id: str,
    severities: str = None,
    names: str = None,
    risk_ids: str = None,
    file_path: str = None,
    search: str = None,
    order_column: str = None,
    order_direction: str = None,
    limit: int = None,
    offset: int = 1,
) -> dict:
    return AiAssetsAPI().get_asset_risks(
        scan_id=scan_id, asset_id=asset_id, severities=severities,
        names=names, risk_ids=risk_ids, file_path=file_path,
        search=search, order_column=order_column,
        order_direction=order_direction, limit=limit, offset=offset,
    )
