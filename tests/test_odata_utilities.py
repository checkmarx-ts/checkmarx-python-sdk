import json

from CheckmarxPythonSDK.CxODataApiSDK import (
    get_project_id_name_and_scan_id_list, get_all_results_with_count_for_each_project_json_format
    )


def test_get_project_id_name_and_scan_id_list():
    r = get_project_id_name_and_scan_id_list()
    assert r is not None


def test_get_all_results_with_count_for_each_project():
    r = get_all_results_with_count_for_each_project_json_format()
    with open("all_results.json", "w") as out_file:
        json.dump(r, out_file, indent=4)
    assert r is not None


def test_get_all_results_with_count_more_than_n_for_each_project():
    n = 20
    r = get_all_results_with_count_for_each_project_json_format(threshold=n)
    with open("results_with_count_more_than_20.json", "w") as out_file:
        json.dump(r, out_file, indent=4)
    assert r is not None


def test_get_all_results_with_count_for_each_project_for_false_positives():
    r = get_all_results_with_count_for_each_project_json_format(filter_false_positive=True)
    with open("false_positive_results.json", "w") as out_file:
        json.dump(r, out_file, indent=4)
    assert r is not None
