"""
Generate a CSV report with all scan results in Checkmarx system
"""
from CheckmarxPythonSDK.CxODataApiSDK import get_results_and_write_to_csv_file


if __name__ == '__main__':
    get_results_and_write_to_csv_file(file_path="all_results.csv")
    print("finish getting all_results")

    get_results_and_write_to_csv_file(file_path="results_with_count_more_than_20.csv", threshold=20)
    print("finish getting results_with_count_more_than_20")

    get_results_and_write_to_csv_file(file_path="false_positive_results.csv", filter_false_positive=True)
    print("finish getting false_positive_results")
