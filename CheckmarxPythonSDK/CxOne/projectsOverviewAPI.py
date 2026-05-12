from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import (
    ProjectCounter,
    ProjectResponseCollection,
)


class ProjectsOverviewAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/projects-overview"
        )

    def get_tenant_projects_overview(
        self,
        offset: int = 0,
        limit: int = 100,
        name: str = None,
        scan_origin: List[str] = None,
        source_type: List[str] = None,
        group_ids: List[str] = None,
        tag_keys: List[str] = None,
        tag_values: List[str] = None,
        risk_level: List[str] = None,
        from_date: str = None,
        to_date: str = None,
        is_deployed: bool = None,
        is_public: bool = None,
        sort: List[str] = ("+last_scanned_at",),
    ) -> ProjectResponseCollection:
        """
        Args:
            offset (int): the request offset
            limit (int): the number of items per page
            name (str): the name of the project
            scan_origin (List[str]): scan origins to filter projects
            source_type (List[str]): source types to filter projects
            group_ids (List[str]): group ids to filter projects
            tag_keys (List[str]): tag keys to filter projects
            tag_values (List[str]): tag values to filter projects
            risk_level (List[str]): risk levels to filter. Available values:
                No Risk, Low, Medium, High, Critical
            from_date (str): start date (2006-01-02T15:04:05Z07:00)
            to_date (str): end date (2006-01-02T15:04:05Z07:00)
            is_deployed (bool): whether the project is deployed in runtime
            is_public (bool): whether the project is publicly exposed
            sort (List[str]): sort criteria. Available values: name,
                scan-origin, last-scan-date, source-type, risk-level,
                is-public. Default: +last_scanned_at

        Returns:
            ProjectResponseCollection
        """
        params = {
            "offset": offset,
            "limit": limit,
            "name": name,
            "scan-origin": scan_origin,
            "source-type": source_type,
            "group-ids": group_ids,
            "tag-keys": tag_keys,
            "tag-values": tag_values,
            "risk-level": risk_level,
            "from-date": from_date,
            "to-date": to_date,
            "is-deployed": is_deployed,
            "is-public": is_public,
            "sort": ",".join(sort) if sort else None,
        }
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        return ProjectResponseCollection.from_dict(response.json())

    def get_project_counters(
        self,
        offset: int = 0,
        limit: int = 100,
        group_by_field: str = "risk-level",
        name: str = None,
        scan_origin: List[str] = None,
        source_type: List[str] = None,
        group_ids: List[str] = None,
        tag_keys: List[str] = None,
        tag_values: List[str] = None,
        empty_tags: bool = None,
        risk_level: List[str] = None,
        from_date: str = None,
        to_date: str = None,
    ) -> List[ProjectCounter]:
        """
        Args:
            offset (int): the request offset
            limit (int): the number of items per page
            group_by_field (str): the field to group by.
                Available values: risk-level
            name (str): the name of the project
            scan_origin (List[str]): scan origins to filter projects
            source_type (List[str]): source types to filter projects
            group_ids (List[str]): group ids to filter projects
            tag_keys (List[str]): tag keys to filter projects
            tag_values (List[str]): tag values to filter projects
            empty_tags (bool):
            risk_level (List[str]): risk levels to filter. Available values:
                No Risk, Low, Medium, High, Critical
            from_date (str): start date (2006-01-02T15:04:05Z07:00)
            to_date (str): end date (2006-01-02T15:04:05Z07:00)

        Returns:
            List[ProjectCounter]
        """
        url = f"{self.base_url}/aggregate"
        params = {
            "offset": offset,
            "limit": limit,
            "group-by-field": group_by_field,
            "name": name,
            "scan-origin": scan_origin,
            "source-type": source_type,
            "group-ids": group_ids,
            "tag-keys": tag_keys,
            "tag-values": tag_values,
            "empty-tags": empty_tags,
            "risk-level": risk_level,
            "from-date": from_date,
            "to-date": to_date,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        item = response.json()
        return [
            ProjectCounter.from_dict(pc)
            for pc in (item.get("projectsCounters") or [])
        ]


def get_tenant_projects_overview(
    offset: int = 0,
    limit: int = 100,
    name: str = None,
    scan_origin: List[str] = None,
    source_type: List[str] = None,
    group_ids: List[str] = None,
    tag_keys: List[str] = None,
    tag_values: List[str] = None,
    risk_level: List[str] = None,
    from_date: str = None,
    to_date: str = None,
    is_deployed: bool = None,
    is_public: bool = None,
    sort: List[str] = ("+last_scanned_at",),
) -> ProjectResponseCollection:
    return ProjectsOverviewAPI().get_tenant_projects_overview(
        offset=offset,
        limit=limit,
        name=name,
        scan_origin=scan_origin,
        source_type=source_type,
        group_ids=group_ids,
        tag_keys=tag_keys,
        tag_values=tag_values,
        risk_level=risk_level,
        from_date=from_date,
        to_date=to_date,
        is_deployed=is_deployed,
        is_public=is_public,
        sort=sort,
    )


def get_project_counters(
    offset: int = 0,
    limit: int = 100,
    group_by_field: str = "risk-level",
    name: str = None,
    scan_origin: List[str] = None,
    source_type: List[str] = None,
    group_ids: List[str] = None,
    tag_keys: List[str] = None,
    tag_values: List[str] = None,
    empty_tags: bool = None,
    risk_level: List[str] = None,
    from_date: str = None,
    to_date: str = None,
) -> List[ProjectCounter]:
    return ProjectsOverviewAPI().get_project_counters(
        offset=offset,
        limit=limit,
        group_by_field=group_by_field,
        name=name,
        scan_origin=scan_origin,
        source_type=source_type,
        group_ids=group_ids,
        tag_keys=tag_keys,
        tag_values=tag_values,
        empty_tags=empty_tags,
        risk_level=risk_level,
        from_date=from_date,
        to_date=to_date,
    )
