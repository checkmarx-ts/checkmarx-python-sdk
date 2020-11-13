"""
Generate a CSV report with all scan results in Checkmarx system
"""
import csv
from CheckmarxPythonSDK.CxODataApiSDK import (ResultsODataAPI, get_project_id_name_and_scan_id_list)
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI, TeamAPI

all_results_field_names = ['TeamFullName', 'ProjectId', 'ProjectName', 'ScanId', 'Language', 'QueryGroup', 'QueryId',
                           'Query', 'ResultId', 'ResultState']
group_by_query_field_names = ['TeamFullName', 'ProjectId', 'ProjectName', 'ScanId', 'Language', 'QueryGroup',
                              'QueryId', 'Query', 'Count']

if __name__ == '__main__':
    teams_api = TeamAPI()
    projects_api = ProjectsAPI()
    results_odata_api = ResultsODataAPI()

    with open('results_with_count_more_than_20.csv', 'w', newline='') as csv_file:
        field_names = group_by_query_field_names
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        project_id_name_and_scan_id_list = get_project_id_name_and_scan_id_list()
        for project in project_id_name_and_scan_id_list:
            project_id = project.get("ProjectId")
            project_name = project.get("ProjectName")
            project_info = projects_api.get_project_details_by_id(project_id=project_id)
            team_id = project_info.team_id
            team_full_name = teams_api.get_team_full_name_by_team_id(team_id=team_id)
            scan_id_list = project.get("ScanIdList")

            for scan_id in scan_id_list:
                # try:
                result_list = results_odata_api.get_results_group_by_query_id(
                    scan_id=scan_id, filter_false_positive=False, threshold=20
                )
                result_list = sorted(result_list,
                                     key=lambda r: (r.get("ResultId"), r.get("Language"), r.get("QueryGroup"),
                                                    r.get("QueryId")))
                for result in result_list:
                    result.update(
                        {
                            "TeamFullName": team_full_name,
                            "ProjectId": project_id,
                            "ProjectName": project_name,
                            "ScanId": scan_id
                        }
                    )
                writer.writerows(result_list)
                # except Exception:
                #     print("Fail to get scan result for scan id: {id}".format(id=scan_id))
