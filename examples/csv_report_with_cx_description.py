import logging
import time
import pathlib

from CheckmarxPythonSDK.CxRestAPISDK.ScansAPI import ScansAPI
from CheckmarxPythonSDK.CxODataApiSDK.ProjectsODataAPI import (
    get_all_projects_id_name
)
from CheckmarxPythonSDK.CxPortalSoapApiSDK.CxPortalWebService import (
    get_query_collection,
    get_cx_description_by_query_id,
    get_query_id_by_language_group_and_query_name,
)

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_command_line_arguments():
    """

    Returns:
        Namespace
    """
    import argparse
    description = 'A simple command-line interface for CxSAST in Python.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--cxsast_base_url', required=True, help="CxSAST base url, for example: https://localhost")
    parser.add_argument('--cxsast_username', required=True, help="CxSAST username")
    parser.add_argument('--cxsast_password', required=True, help="CxSAST password")
    parser.add_argument('--project_names', required=True, help="example: project1,project2")
    parser.add_argument('--report_file_path', default=None, help="csv report file path")
    return parser.parse_known_args()


def generate_report(scan_id: int, project_name: str, report_file_path: str):
    """

    Args:
        scan_id (int):
        project_name (str):
        report_file_path (str):

    Returns:
        str
    """
    logger.info(f"begin to generate csv report, at location: {file_path}")
    from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI
    scan_api = ScansAPI()

    logger.info("register scan report")
    report = scan_api.register_scan_report(scan_id=scan_id, report_type="CSV")
    report_id = report.report_id
    logger.info("report_id : {}".format(report_id))

    logger.info("get report status by id")
    while not scan_api.is_report_generation_finished(report_id):
        logger.info("report generating")
        time.sleep(10)

    logger.info("get report by id")
    report_content = scan_api.get_report_by_id(report_id)

    logger.info("write original report")
    default_file_name = f"/{project_name}_csv_report_with_description.csv"
    if report_file_path is None:
        report_path = "." + default_file_name
    path = pathlib.Path(report_file_path)
    if path.is_dir():
        report_file_path += default_file_name
    with open(str(report_file_path), "wb") as f_out:
        f_out.write(report_content)
    logger.info(f"finish generate csv report for scan id {scan_id}, report file path: {report_file_path}")
    return report_file_path


def update_csv_report(cx_report_file_path, query_collections, query_description_func):
    """
    update CSV report by add the similarityID column (data retrieved by using ODATA API)
    Args:
        cx_report_file_path:
        query_collections:
        query_description_func:

    Returns:

    """
    logger.info("update csv report")
    if not pathlib.Path(cx_report_file_path).exists():
        logger.info(f"report does not exist, file path: {cx_report_file_path}")
        return
    import csv
    from collections import OrderedDict

    logger.info("read csv file")
    new_field_name = 'CxDescription'
    csv_content = []
    with open(cx_report_file_path, newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        field_names = reader.fieldnames
        field_names = [item for item in field_names]
        field_names.append(new_field_name)
        for row in reader:
            query_name = "_".join(row.get("Query").split(" "))
            query_path = row.get("QueryPath")
            query_path_list = query_path.split(":")[0].replace("Version", "").strip().split("\\")
            language = query_path_list[0]
            package_type_name = "_".join(query_path_list[1].split(" "))
            package_name = "_".join(query_path_list[2].split(" "))
            query_id = get_query_id_by_language_group_and_query_name(query_collections, language, package_type_name,
                                                                     package_name,
                                                                     query_name)
            query_description = query_description_func(query_id)
            new_ordered_dict = OrderedDict()
            for key, value in row.items():
                new_ordered_dict[key] = value
            new_ordered_dict[new_field_name] = query_description
            csv_content.append(new_ordered_dict)
    logger.info("write csv file")
    with open(cx_report_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, dialect='unix')
        writer.writeheader()
        writer.writerows(csv_content)


if __name__ == '__main__':
    cli_args = get_command_line_arguments()
    cli_args = cli_args[0]
    file_path = cli_args.report_file_path
    project_names = cli_args.project_names
    project_names = project_names.split(",") if ',' in project_names else [project_names]
    project_id_names = get_all_projects_id_name()
    query_description_function = get_cx_description_by_query_id()
    query_collections = get_query_collection().get("QueryGroups")
    for project_name in project_names:
        logger.info(f"generate csv report for project: {project_name}")
        project_id = None
        filtered_projects = [item for item in project_id_names if item.get("ProjectName") == project_name]
        if len(filtered_projects) == 1:
            project_id = filtered_projects[0].get("ProjectId")
        if project_id is None:
            logger.info(f"project with name {project_name} does not exist!")
            continue
        scan_id = ScansAPI.get_last_scan_id_of_a_project(project_id,
                                                         only_finished_scans=True,
                                                         only_completed_scans=True,
                                                         only_real_scans=True,
                                                         only_full_scans=False,
                                                         only_public_scans=True
                                                         )
        logger.info(f"get scan id: {scan_id}")
        report_file_path = generate_report(scan_id=scan_id, project_name=project_name, report_file_path=file_path)
        update_csv_report(cx_report_file_path=report_file_path, query_collections=query_collections,
                          query_description_func=query_description_function)
