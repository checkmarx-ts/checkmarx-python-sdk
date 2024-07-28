# encoding: utf-8
from .httpRequests import get_request
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import (
    ProjectResponseModel,
    SeverityCounter,
    TotalCounters,
    EngineData,
    ProjectCounter,
)

api_url = "/api/projects-overview"


def construct_project_response(project):
    return ProjectResponseModel(
        project_id=project.get("projectId"),
        project_name=project.get("projectName"),
        source_origin=project.get("sourceOrigin"),
        last_scan_date=project.get("lastScanDate"),
        source_type=project.get("sourceType"),
        tags=project.get("tags"),
        groups_ids=project.get("groupIds"),
        risk_level=project.get("riskLevel"),
        repo_id=project.get("repoId"),
        scm_repo_id=project.get("scmRepoId"),
        total_counters=TotalCounters(
            severity_counters=[
                SeverityCounter(
                    severity=severity_counter.get("severity"),
                    counter=severity_counter.get("counter"),
                ) for severity_counter in project.get("totalCounters").get("severityCounters", []) or []
            ]
        ),
        engines_data=[
            EngineData(
                engine=engine_data.get("engine"),
                risk_level=engine_data.get("riskLevel"),
                last_scan_id=engine_data.get("lastScanId"),
                severity_counters=[
                    SeverityCounter(
                        severity=severity_counter.get("severity"),
                        counter=severity_counter.get("counter"),
                    ) for severity_counter in engine_data.get("severityCounters")
                ]
            ) for engine_data in project.get("enginesData")
        ],
    )


def get_tenant_projects_overview(offset=0, limit=100, name=None, scan_origin=None, source_type=None, group_ids=None,
                                 tag_keys=None, tag_values=None, risk_level=None, from_date=None, to_date=None,
                                 is_deployed=None, is_public=None, sort=None):
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
        sort (list of str): A comma-separated list of sort criteria. Each criterion is formatted as '+field,-field2' or
                '-field,+field2' where 'field' and 'filed2 are the names of the fields to sort by and '+' or '-'
                specifies descending or ascending order.
                Available values : name, scan-origin, last-scan-date, source-type, risk-level, is-public
                Default value : +last_scanned_at
                Example : +name,-scan-origin

    Returns:

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

    relative_url += "?offset={}&limit={}".format(offset, limit)
    if name:
        relative_url += "&name={}".format(name)
    if scan_origin:
        relative_url += "&scan-origin={}".format(scan_origin)
    if source_type:
        relative_url += "&source-type={}".format(source_type)
    if group_ids:
        relative_url += "&group-ids={}".format(group_ids)
    if tag_keys:
        relative_url += "&tag-keys={}".format(tag_keys)
    if tag_values:
        relative_url += "&tag-values={}".format(tag_values)
    if risk_level:
        relative_url += "&risk-level={}".format(risk_level)
    if from_date:
        relative_url += "&from-date={}".format(from_date)
    if to_date:
        relative_url += "&to-date={}".format(to_date)
    if is_deployed:
        relative_url += "&is-deployed={}".format(is_deployed)
    if is_public:
        relative_url += "&is-public={}".format(is_public)
    if sort:
        relative_url += "&sort={}".format(sort)

    response = get_request(relative_url=relative_url)
    item = response.json()
    return {
        "totalCount": item.get("totalCount"),
        "projects": [
           construct_project_response(project) for project in item.get("projects")
        ]
    }


def get_project_counters(offset=0, limit=100, group_by_field="risk-level", name=None, scan_origin=None,
                         source_type=None, group_ids=None, tag_keys=None, tag_values=None, risk_level=None,
                         from_date=None, to_date=None,):
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
            risk_level (list of str): a list of risk levels to filter projects
                                Available values : No Risk, Low, Medium, High, Critical
            from_date (str):  the start date to filter projects: 2006-01-02T15:04:05Z07:00
            to_date (str): the end date to filter projects: 2006-01-02T15:04:05Z07:00

        Returns:

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
    relative_url += "?offset={}&limit={}&group-by-field={}".format(offset, limit, group_by_field)

    if name:
        relative_url += "&name={}".format(name)
    if scan_origin:
        relative_url += "&scan-origin={}".format(scan_origin)
    if source_type:
        relative_url += "&source-type={}".format(source_type)
    if group_ids:
        relative_url += "&group-ids={}".format(group_ids)
    if tag_keys:
        relative_url += "&tag-keys={}".format(tag_keys)
    if tag_values:
        relative_url += "&tag-values={}".format(tag_values)
    if risk_level:
        relative_url += "&risk-level={}".format(risk_level)
    if from_date:
        relative_url += "&from-date={}".format(from_date)
    if to_date:
        relative_url += "&to-date={}".format(to_date)

    response = get_request(relative_url=relative_url)
    item = response.json()
    return [
        ProjectCounter(
            value=project_counter.get("value"),
            count=project_counter.get("count"),
        ) for project_counter in item.get("projectsCounters")
    ]
