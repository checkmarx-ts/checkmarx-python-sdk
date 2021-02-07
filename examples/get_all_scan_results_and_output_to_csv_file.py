"""
Generate a CSV report with all scan results in Checkmarx system
"""
from CheckmarxPythonSDK.CxODataApiSDK import (
    dump_last_scan_results_of_each_project_into_csv_file,
    dump_last_scan_results_statistics_of_each_project_into_csv_file
)

if __name__ == '__main__':
    dump_last_scan_results_of_each_project_into_csv_file(file_path="all_results.csv")
    print("finish getting all_results")

    dump_last_scan_results_statistics_of_each_project_into_csv_file(file_path="results_with_count_more_than_20.csv",
                                                                    threshold=20)
    print("finish getting results_with_count_more_than_20")

    dump_last_scan_results_statistics_of_each_project_into_csv_file(file_path="false_positive_results.csv")
    print("finish getting false_positive_results")
