import csv
from itertools import groupby
from copy import deepcopy

from .ProjectsODataAPI import ProjectsODataAPI
from .ScansODataAPI import ScansODataAPI
from .ResultsODataAPI import ResultsODataAPI


def get_project_id_name_and_scan_id_list():
    """

    Returns:
        list of dict

        example:
        [
        {'ProjectId': 10, 'ProjectName': 'jvl_local', 'ScanIdList': [1000008, 1000012]},
        {'ProjectId': 16, 'ProjectName': 'mybatis-test', 'ScanIdList': [1000015]}
        ]
    """
    projects_odata_api = ProjectsODataAPI()
    scans_odata_api = ScansODataAPI()

    project_id_name_list = projects_odata_api.get_all_projects_id_name()
    for project_id_name in project_id_name_list:
        project_id = project_id_name.get("ProjectId")
        scan_id_list = scans_odata_api.get_all_scan_id_of_a_project(project_id=project_id)
        project_id_name.update(
            {
                "ScanIdList": list(scan_id_list)
            }
        )

    project_id_name_and_scan_id_list = project_id_name_list

    return project_id_name_and_scan_id_list


def scan_results_group_by_query_id(original_results):
    """

    Returns:

    """
    results = []
    original_results = sorted(original_results, key=lambda r: r.get("QueryId"))
    for _, query_id_group in groupby(original_results, lambda r: r.get("QueryId")):
        list_of_result_with_same_query_id = list(query_id_group)
        count = len(list_of_result_with_same_query_id)

        first_dict = deepcopy(list_of_result_with_same_query_id[0])
        first_dict.pop("ResultId")
        first_dict.pop("ResultState")
        first_dict.update({"Count": count})

        results.append(first_dict)

    return results


def get_all_results_with_count_for_each_project_json_format(filter_false_positive=False, threshold=0):
    """
    Warnings: this function put all data in one big dict, if you have a lot of projects in your
    Checkmarx system, this function may fail.

    Returns:

    """
    results_odata_api = ResultsODataAPI()
    project_id_name_and_scan_id_list = get_project_id_name_and_scan_id_list()

    for project in project_id_name_and_scan_id_list:
        scan_id_list = project.get("ScanIdList")

        results_list = []
        for scan_id in scan_id_list:

            try:
                results_with_query = results_odata_api.get_results_group_by_query_id_and_add_count_json_format(
                    scan_id=scan_id, filter_false_positive=filter_false_positive, threshold=threshold
                )

                results_list.append(
                    {
                        "ScanId": scan_id,
                        "ResultsWithQuery": results_with_query
                    }
                )
            except Exception:
                print("Fail to fetch data for scan id: {id} ".format(id=scan_id))

        project.update(
            {
                "Scans": results_list
            }
        )

    return project_id_name_and_scan_id_list


def get_results_and_write_to_csv_file(file_path, filter_false_positive=False, threshold=0):
    """
    Args:
        file_path (str):
        filter_false_positive (bool): True if get only [Proposed] Not Exploitable results,
                                        otherwise get all result state
        threshold (int): minimum number of count for results

    Returns:

    """
    projects_odata_api = ProjectsODataAPI()
    scans_odata_api = ScansODataAPI()
    results_odata_api = ResultsODataAPI()

    common_field_names = ['ProjectId', 'ProjectName', 'ScanId', 'Language', 'QueryGroup', 'QueryId', 'Query']

    all_results_field_names = common_field_names[:]
    all_results_field_names.extend(['ResultId', 'ResultState'])

    group_by_query_field_names = common_field_names[:]
    group_by_query_field_names.extend(['Count'])

    with open(file_path, 'w', newline='') as csv_file:

        is_for_all_results = True if filter_false_positive is False and threshold == 0 else False

        field_names = all_results_field_names if is_for_all_results else group_by_query_field_names

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        project_id_name_list = projects_odata_api.get_all_projects_id_name()
        for project in project_id_name_list:
            project_id = project.get("ProjectId")
            project_name = project.get("ProjectName")

            try:
                last_scan_id = scans_odata_api.get_the_scan_id_of_last_scan(project_id=project_id)
            except Exception:
                print("Project name: {name}, id : {id} has no scans".format(name=project_name, id=project_id))
                continue

            try:
                result_list = results_odata_api.get_results_for_a_specific_scan_id_with_query_language_state(
                    scan_id=last_scan_id, filter_false_positive=filter_false_positive
                )
            except Exception:
                print("Fail to get scan result for scan id: {id}".format(id=last_scan_id))
                continue

            if is_for_all_results:
                result_list = sorted(
                    result_list, key=lambda r: (r.get("Language"),
                                                r.get("QueryGroup"), r.get("QueryId"), r.get("ResultId"))
                    )
            else:
                result_list = scan_results_group_by_query_id(result_list)
                result_list = sorted(result_list, key=lambda r: (r.get("Language"), r.get("QueryGroup"),
                                                                 r.get("QueryId"),))

                if threshold > 1:
                    result_list = list(filter(lambda r: r.get("Count") >= threshold, result_list))

            for result in result_list:
                result.update(
                    {
                        "ProjectId": project_id,
                        "ProjectName": project_name,
                        "ScanId": last_scan_id
                    }
                )
            writer.writerows(result_list)
