import csv
from itertools import groupby
from copy import deepcopy

from .ProjectsODataAPI import (get_all_projects_id_name, get_all_projects_id_name_and_team_id_name)
from .ScansODataAPI import (
    get_all_scan_id_of_a_project,
    get_last_scan_id_of_a_project,
    get_last_full_scan_id_of_a_project
)
from .ResultsODataAPI import (
    ResultsODataAPI,
    get_results_group_by_query_id_and_add_count_json_format,
    get_results_for_a_specific_scan_id_with_query_language_state,
)


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
    project_id_name_list = get_all_projects_id_name()
    for project_id_name in project_id_name_list:
        project_id = project_id_name.get("ProjectId")
        scan_id_list = get_all_scan_id_of_a_project(project_id=project_id)
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
        total_number_of_same_query_result = len(list_of_result_with_same_query_id)
        false_positive_number = len(
            list(filter(lambda r: r.get("ResultState") in ["Not Exploitable", "Proposed Not Exploitable"],
                        list_of_result_with_same_query_id)))

        first_dict = deepcopy(list_of_result_with_same_query_id[0])
        first_dict.pop('SimilarityId')
        first_dict.pop("ResultId")
        first_dict.pop("ResultState")
        first_dict.update({"TotalNumber": total_number_of_same_query_result})
        first_dict.update({"FalsePositiveNumber": false_positive_number})

        results.append(first_dict)

    return results


def get_all_results_with_count_for_each_project_json_format(filter_false_positive=False, threshold=0):
    """
    Warnings: this function put all data in one big dict, if you have a lot of projects in your
    Checkmarx system, this function may fail.

    Returns:

    """
    project_id_name_and_scan_id_list = get_project_id_name_and_scan_id_list()

    for project in project_id_name_and_scan_id_list:
        scan_id_list = project.get("ScanIdList")

        results_list = []
        for scan_id in scan_id_list:

            try:
                results_with_query = get_results_group_by_query_id_and_add_count_json_format(
                    scan_id=scan_id, filter_false_positive=filter_false_positive, threshold=threshold
                )

                results_list.append(
                    {
                        "ScanId": scan_id,
                        "ResultsWithQuery": results_with_query
                    }
                )
            except ValueError as e:
                print(e)
                print("Fail to fetch data for scan id: {id} ".format(id=scan_id))

        project.update(
            {
                "Scans": results_list
            }
        )

    return project_id_name_and_scan_id_list


def merge_results_by_similarity_id(first_result_list, second_result_list):
    """

    use first as base, merge the second into the first one.

    Args:
        first_result_list (list of dict): example
         [
          {'SimilarityId': 614020830, 'Language': 'Java', 'QueryGroup': 'Java_Best_Coding_Practice',
          'Query': 'Portability_Flaw_In_File_Separator', 'QueryId': 3591, 'ResultId': 908, 'ResultState': 'To Verify'},
          {'SimilarityId': 994470032, 'Language': 'Java', 'QueryGroup': 'Java_High_Risk',
          'Query': 'Connection_String_Injection', 'QueryId': 589, 'ResultId': 4,
          'ResultState': 'Proposed Not Exploitable'},
          {'SimilarityId': -1538906028, 'Language': 'Java', 'QueryGroup': 'Java_High_Risk',
          'Query': 'Connection_String_Injection', 'QueryId': 589, 'ResultId': 5, 'ResultState': 'Not Exploitable'},
         ]
        second_result_list (list of dict):
        [
        {'SimilarityId': 994470032, 'Language': 'Java', 'QueryGroup': 'Java_High_Risk',
        'Query': 'Connection_String_Injection', 'QueryId': 589, 'ResultId': 16,
        'ResultState': 'Proposed Not Exploitable'},
        {'SimilarityId': 1937265109, 'Language': 'Java', 'QueryGroup': 'Java_High_Risk',
        'Query': 'Connection_String_Injection', 'QueryId': 589, 'ResultId': 17, 'ResultState': 'To Verify'},
        {'SimilarityId': 646035161, 'Language': 'Java', 'QueryGroup': 'Java_High_Risk',
        'Query': 'Connection_String_Injection', 'QueryId': 589, 'ResultId': 18, 'ResultState': 'To Verify'},
        ]
    Returns:
        list of dict
    """
    similarity_id_list_of_first = [item.get('SimilarityId') for item in first_result_list]

    for item in second_result_list:
        if item.get('SimilarityId') in similarity_id_list_of_first:
            continue
        first_result_list.append(item)

    return first_result_list


def get_result(project, filter_false_positive=False, threshold=0):
    
    is_for_all_raw_results = True if filter_false_positive is False and threshold == 0 else False

    team_id = project.get("TeamId")
    team_name = project.get("TeamName")
    project_id = project.get("ProjectId")
    project_name = project.get("ProjectName")

    last_scan_id = get_last_scan_id_of_a_project(project_id=project_id)
    if not last_scan_id:
        print("Project name: {name}, id : {id} has no scans".format(name=project_name, id=project_id))
        return None
    
    last_full_scan_id = get_last_full_scan_id_of_a_project(project_id=project_id)

    try:
        result_list = get_results_for_a_specific_scan_id_with_query_language_state(scan_id=last_scan_id)
    except ValueError as e:
        print("Fail to get scan result for scan id: {id}".format(id=last_scan_id))
        print("Exception: {error} ".format(error=e))
        return None

    if last_scan_id != last_full_scan_id:
        try:
            last_full_scan_result = get_results_for_a_specific_scan_id_with_query_language_state(
                scan_id=last_full_scan_id
            )
        except Exception as e:
            print("Fail to get scan result for scan id: {id}".format(id=last_full_scan_id))
            print("Exception: {error} ".format(error=e))
            return None

        result_list = merge_results_by_similarity_id(result_list, last_full_scan_result)

    if is_for_all_raw_results:
        result_list = sorted(
            result_list, key=lambda r: (r.get("Language"),
                                        r.get("QueryGroup"), r.get("QueryId"), r.get("ResultId"))
        )
    else:
        result_list = scan_results_group_by_query_id(result_list)
        result_list = sorted(result_list, key=lambda r: (r.get("Language"), r.get("QueryGroup"),
                                                         r.get("QueryId"),))

        if threshold > 1:
            result_list = list(filter(lambda r: r.get("TotalNumber") >= threshold, result_list))

    for result in result_list:
        result.update(
            {
                "TeamName": team_name,
                "TeamId": team_id,
                "ProjectId": project_id,
                "ProjectName": project_name,
                "ScanId": last_scan_id,
                "DirectLink": f"{ResultsODataAPI().api_client.configuration.server_base_url}/cxwebclient"
                              f"/ViewerMain.aspx?scanid={last_scan_id}&projectid={project_id}"
                              f"&pathid={result.get("PathId")}"
            }
        )

    return result_list


def get_results_and_write_to_csv_file(file_path, field_names, filter_false_positive=False, threshold=0):
    """
    Args:
        file_path (str):
        field_names (list of str):
        filter_false_positive (bool): True if get only [Proposed] Not Exploitable results,
                                        otherwise get all result state
        threshold (int): minimum number for results

    Returns:

    """

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        for project in get_all_projects_id_name_and_team_id_name():
            results = get_result(project, filter_false_positive, threshold)
            if not results:
                continue
            writer.writerows(results)


def dump_last_scan_results_of_each_project_into_csv_file(file_path):
    filed_names = ['TeamName', 'TeamId', 'ProjectId', 'ProjectName', 'ScanId', 'Language', 'QueryGroup',
                   'QueryId', 'Query', 'SimilarityId', 'ResultId', 'ResultState', "Origin", "LOC", "PathId",
                   "DirectLink"]
    get_results_and_write_to_csv_file(file_path=file_path, field_names=filed_names)


def dump_last_scan_results_statistics_of_each_project_into_csv_file(file_path, threshold=0):
    filed_names = ['TeamName', 'TeamId', 'ProjectId', 'ProjectName', 'ScanId', 'Language', 'QueryGroup',
                   'QueryId', 'Query', 'TotalNumber', 'FalsePositiveNumber', "Origin", "LOC", "PathId",
                   "DirectLink"]
    get_results_and_write_to_csv_file(file_path=file_path, field_names=filed_names, filter_false_positive=True,
                                      threshold=threshold)
