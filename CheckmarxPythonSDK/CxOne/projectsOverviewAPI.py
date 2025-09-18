from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .utilities import type_check, list_member_type_check
from typing import List
from .dto import (
    ProjectCounter, construct_project_counter,
    ProjectResponseCollection, construct_project_response_collection,
)

api_url = "/api/projects-overview"


class ProjectsOverviewAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_tenant_projects_overview(
            self, offset: int = 0, limit: int = 100, name: str = None, scan_origin: List[str] = None,
            source_type: List[str] = None, group_ids: List[str] = None, tag_keys: List[str] = None,
            tag_values: List[str] = None, risk_level: List[str] = None, from_date: str = None,
            to_date: str = None, is_deployed: bool = None, is_public: bool = None,
            sort: List[str] = ("+last_scanned_at",)
    ) -> ProjectResponseCollection:
        """

        Args:
            offset (int): the request offset
            limit (int): the number of items per page
            name (str): the name of the project
            scan_origin (list of str): a list of scan origins to filter projects
            source_type (list of str): a list of source type to filter projects
            group_ids (list of str): a list of group ids to filter projects
            tag_keys (list of str): a list of tag keys to filter projects
            tag_values (list of str): a list of tag values to filter projects
            risk_level (list of str): a list of risk levels to filter projects
                                Available values : No Risk, Low, Medium, High, Critical
            from_date (str):  the start date to filter projects: 2006-01-02T15:04:05Z07:00
            to_date (str): the end date to filter projects: 2006-01-02T15:04:05Z07:00
            is_deployed (bool): whether the project is deployed in runtime or not
            is_public (bool): whether the project is publicly exposed in runtime or not
            sort (list of str): A comma-separated list of sort criteria. Each criterion is formatted as '+field,-field2'
                    or '-field,+field2' where 'field' and 'filed2 are the names of the fields to sort by and '+' or '-'
                    specifies descending or ascending order.
                    Available values : name, scan-origin, last-scan-date, source-type, risk-level, is-public
                    Default value : +last_scanned_at
                    Example : +name,-scan-origin

        Returns:
            ProjectResponseCollection
        """
        relative_url = api_url
        type_check(offset, int)
        type_check(limit, int)
        type_check(name, str)
        type_check(scan_origin, list)
        list_member_type_check(scan_origin, str)
        type_check(source_type, list)
        list_member_type_check(source_type, str)
        type_check(group_ids, list)
        list_member_type_check(group_ids, str)
        type_check(tag_keys, list)
        list_member_type_check(tag_keys, str)
        type_check(tag_values, list)
        list_member_type_check(tag_values, str)
        type_check(risk_level, list)
        list_member_type_check(risk_level, str)
        type_check(from_date, str)
        type_check(to_date, str)
        type_check(is_deployed, bool)
        type_check(is_public, bool)
        type_check(sort, list)
        list_member_type_check(sort, str)
        params = {
            "offset": offset, "limit": limit, "name": name, "scan-origin": scan_origin, "source-type": source_type,
            "group-ids": group_ids, "tag-keys": tag_keys, "tag-values": tag_values, "risk-level": risk_level,
            "from-date": from_date, "to-date": to_date, "is-deployed": is_deployed, "is-public": is_public,
            "sort": ",".join(sort) if sort else None,
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return construct_project_response_collection(response.json())

    def get_project_counters(
            self, offset: int = 0, limit: int = 100, group_by_field: str = "risk-level", name: str = None,
            scan_origin: List[str] = None, source_type: List[str] = None, group_ids: List[str] = None,
            tag_keys: List[str] = None, tag_values: List[str] = None, empty_tags: bool = None,
            risk_level: List[str] = None, from_date: str = None, to_date: str = None
    ) -> List[ProjectCounter]:
        """

        Args:
            offset (int): the request offset
            limit (int): the number of items per page
            group_by_field (str): the field to group by. Available values : risk-level
            name (str): the name of the project
            scan_origin (list of str): a list of scan origins to filter projects
            source_type (list of str): a list of source type to filter projects
            group_ids (list of str): a list of group ids to filter projects
            tag_keys (list of str): a list of tag keys to filter projects
            tag_values (list of str): a list of tag values to filter projects
            empty_tags (bool):
            risk_level (list of str): a list of risk levels to filter projects
                                Available values : No Risk, Low, Medium, High, Critical
            from_date (str):  the start date to filter projects: 2006-01-02T15:04:05Z07:00
            to_date (str): the end date to filter projects: 2006-01-02T15:04:05Z07:00

        Returns:
            List[ProjectCounter]
        """
        relative_url = api_url + "/aggregate"
        type_check(offset, int)
        type_check(limit, int)
        type_check(group_by_field, str)
        type_check(name, str)
        type_check(scan_origin, list)
        list_member_type_check(scan_origin, str)
        type_check(source_type, list)
        list_member_type_check(source_type, str)
        type_check(group_ids, list)
        list_member_type_check(group_ids, str)
        type_check(tag_keys, list)
        list_member_type_check(tag_keys, str)
        type_check(tag_values, list)
        list_member_type_check(tag_values, str)
        type_check(risk_level, list)
        list_member_type_check(risk_level, str)
        type_check(from_date, str)
        type_check(to_date, str)
        params = {
            "offset": offset, "limit": limit, "group-by-field": group_by_field,
            "name": name, "scan-origin": scan_origin, "source-type": source_type,
            "group-ids": group_ids, "tag-keys": tag_keys, "tag-values": tag_values,
            "empty-tags": empty_tags,
            "risk-level": risk_level,
            "from-date": from_date, "to-date": to_date,
        }

        response = self.api_client.get_request(relative_url=relative_url, params=params)
        item = response.json()
        return [
            construct_project_counter(project_counter) for project_counter in item.get("projectsCounters")
        ]


def get_tenant_projects_overview(
        offset: int = 0, limit: int = 100, name: str = None, scan_origin: List[str] = None,
        source_type: List[str] = None, group_ids: List[str] = None, tag_keys: List[str] = None,
        tag_values: List[str] = None, risk_level: List[str] = None, from_date: str = None, to_date: str = None,
        is_deployed: bool = None, is_public: bool = None, sort: List[str] = ("+last_scanned_at",)
) -> ProjectResponseCollection:
    return ProjectsOverviewAPI().get_tenant_projects_overview(
        offset=offset, limit=limit, name=name, scan_origin=scan_origin, source_type=source_type, group_ids=group_ids,
        tag_keys=tag_keys, tag_values=tag_values, risk_level=risk_level, from_date=from_date, to_date=to_date,
        is_deployed=is_deployed, is_public=is_public, sort=sort
    )


def get_project_counters(
        offset: int = 0, limit: int = 100, group_by_field: str = "risk-level", name: str = None,
        scan_origin: List[str] = None, source_type: List[str] = None, group_ids: List[str] = None,
        tag_keys: List[str] = None, tag_values: List[str] = None, empty_tags: bool = None, risk_level: List[str] = None,
        from_date: str = None, to_date: str = None
) -> List[ProjectCounter]:
    return ProjectsOverviewAPI().get_project_counters(
        offset=offset, limit=limit, group_by_field=group_by_field, name=name, scan_origin=scan_origin,
        source_type=source_type, group_ids=group_ids, tag_keys=tag_keys, tag_values=tag_values,
        empty_tags=empty_tags, risk_level=risk_level, from_date=from_date, to_date=to_date
    )
