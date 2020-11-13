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
        scan_id_list = scans_odata_api.get_scan_id_list_for_one_project(project_id=project_id)
        project_id_name.update(
            {
                "ScanIdList": list(scan_id_list)
            }
        )

    project_id_name_and_scan_id_list = project_id_name_list

    return project_id_name_and_scan_id_list


def get_all_results_with_count_for_each_project(filter_false_positive=False, threshold=0):
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
