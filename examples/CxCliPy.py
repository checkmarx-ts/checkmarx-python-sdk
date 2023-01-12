"""
This a CLI script. It can be converted to binary file by using pyinstaller

pyinstaller -y -F --clean CxCliPy.py

Sample usage
/home/happy/Documents/CxCliPy/dist/CxCliPy scan --cxsast_base_url http://192.168.3.84 --cxsast_username Admin
--cxsast_password *** --preset All --incremental False --location_type Folder
--location_path /home/happy/Documents/JavaVulnerableLab
--project_name /CxServer/happy-2022-11-21 --exclude_folders "test" --report_csv cx-report.csv
"""
import pathlib
import time
import os
from os.path import exists
from zipfile import ZipFile, ZIP_DEFLATED
import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_cx_supported_file_extensions():
    return [
        '.apex', '.apexp', '.asax', '.ascx', '.asp', '.aspx', '.bas', '.bdy', '.c', '.c++', '.cc', '.cgi', '.cls',
        '.component', '.conf', '.config', '.cpp', '.cs', '.cshtml', '.csproj', '.ctl', '.ctp', '.cxx', '.dsr', '.ec',
        '.erb', '.fnc', '.frm', '.go', '.gradle', '.groovy', '.gsh', '.gsp', '.gtl', '.gvy', '.gy', '.h', '.h++',
        '.handlebars', '.hbs', '.hh', '.hpp', '.htm', '.html', '.hxx', '.inc', '.jade', '.java', '.javasln', '.js',
        '.jsf', '.json', '.jsp', '.jspf', '.lock', '.m', '.master', '.-meta.xml', '.mf', '.object', '.page', '.pc',
        '.pck', '.php', '.php3', '.php4', '.php5', '.phtm', '.phtml', '.pkb', '.pkh', '.pks', '.pl', '.plist', '.pls',
        '.plx', '.pm', '.prc', '.project', '.properties', '.psgi', '.py', '.rb', '.report', '.rhtml', '.rjs', '.rxml',
        '.scala', '.should_neve_match_anything_9gdfg4', '.sln', '.spc', '.sqb', '.sqf', '.sqh', '.sql', '.sqp', '.sqt',
        '.sqtb', '.sqth', '.sqv', '.swift', '.tag', '.tgr', '.tld', '.tpb', '.tpl', '.tps', '.trg', '.trigger', '.ts',
        '.tsx', '.twig', '.vb', '.vbp', '.vbs', '.wod', '.workflow', '.xaml', '.xhtml', '.xib', '.xml', '.xsaccess',
        '.xsapp', '.xsjs', '.xsjslib', '-meta.xml'
    ]


def get_command_line_arguments():
    """

    Returns:
        Namespace
    """
    import argparse
    description = 'A simple command-line interface for CxSAST in Python.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('scan')
    parser.add_argument('--cxsast_base_url', required=True, help="CxSAST base url, for example: https://localhost")
    parser.add_argument('--cxsast_username', required=True, help="CxSAST username")
    parser.add_argument('--cxsast_password', required=True, help="CxSAST password")
    parser.add_argument('-preset', '--preset', required=True, help="The preset (rule set) name")
    parser.add_argument('-incremental', '--incremental', default=False, help="Set it True for incremental scan")
    parser.add_argument('-location_type', '--location_type', required=True, help="Folder, Git")
    parser.add_argument('-location_path', '--location_path', required=True, help="Source code folder absolute path")
    parser.add_argument('-project_name', '--project_name', required=True, help="Checkmarx project full path")
    parser.add_argument('-exclude_folders', '--exclude_folders', help="exclude folders")
    parser.add_argument('-exclude_files', '--exclude_files', help='exclude files')
    parser.add_argument('-report_xml', '--report_xml', default=None, help="xml report file path")
    parser.add_argument('-report_pdf', '--report_pdf', default=None, help="pdf report file path")
    parser.add_argument('-report_csv', '--report_csv', default=None, help="csv report file path")
    parser.add_argument('-full_scan_cycle', '--full_scan_cycle', default=10,
                        help="Defines the number of incremental scans to be performed, before performing a periodic "
                             "full scan")
    return parser.parse_known_args()


def create_zip_file_from_location_path(location_path_str: str, project_name: str):
    """

    Args:
        location_path_str (str):
        project_name (str)

    Returns:
        str (ZIP file path)
    """
    from pathlib import Path
    import tempfile
    temp_dir = tempfile.gettempdir()
    extensions = get_cx_supported_file_extensions()
    path = Path(location_path_str)
    if not path.exists():
        raise FileExistsError(f"{location_path_str} does not exist, abort scan")
    file_path = f"{temp_dir}/cx_{project_name}.zip"
    with ZipFile(file_path, "w", ZIP_DEFLATED) as zip_file:
        root_len = len(location_path_str) + 1
        for base, dirs, files in os.walk(location_path_str):
            if ".git" in base or ".idea" in base or ".settings" in base or "bin" in base or "target" in base \
                    or "images" in base:
                continue
            for file in files:
                if file.startswith(".") and not file.endswith(tuple(extensions)):
                    continue
                fn = os.path.join(base, file)
                zip_file.write(fn, fn[root_len:])
    return file_path


def cx_scan_from_local_zip_file(preset_name: str, team_full_name: str, project_name: str, zip_file_path: str,
                                exclude_folders: str, exclude_files: str, incremental: bool = False,
                                full_scan_cycle=10):
    """

    Args:
        preset_name (str):
        team_full_name (str):
        project_name (str):
        zip_file_path (str):
        exclude_folders (str):
        exclude_files (str):
        incremental (bool):
        full_scan_cycle (int):

    Returns:

    """
    from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI, ProjectsAPI, ScansAPI
    team_api = TeamAPI()
    projects_api = ProjectsAPI()
    scan_api = ScansAPI()

    if not exists(zip_file_path):
        logger.error("[ERROR]: zip file not found. Abort scan.")
        exit(1)

    logger.info("get team id")
    team_id = team_api.get_team_id_by_team_full_name(team_full_name)
    if not team_id:
        logger.error(f"[ERROR]: team full name {team_full_name} not exist. Abort scan.")
        exit(1)

    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(
        project_name=project_name, team_full_name=team_full_name
    )
    logger.info(f"project id: {project_id}")
    if not project_id:
        logger.info("project does not exist. create project with default configuration, will get project id")
        project = projects_api.create_project_with_default_configuration(project_name=project_name, team_id=team_id)
        project_id = project.id
        logger.info(f"new project with project_id: {project_id}")

    logger.info("upload source code zip file")
    projects_api.upload_source_code_zip_file(project_id, str(zip_file_path))

    logger.info("define SAST scan settings, set preset")
    preset_id = projects_api.get_preset_id_by_name(preset_name=preset_name)
    logger.info("preset id: {}".format(preset_id))
    scan_api.define_sast_scan_settings(project_id=project_id, preset_id=preset_id)

    logger.info("set exclude folders and exclude files")
    projects_api.set_project_exclude_settings_by_project_id(
        project_id, exclude_folders_pattern=exclude_folders, exclude_files_pattern=exclude_files
    )

    scans_of_this_project = scan_api.get_all_scans_for_project(project_id=project_id)
    number_of_scans_of_this_project = len(scans_of_this_project) + 1
    remainder = number_of_scans_of_this_project % full_scan_cycle
    if remainder == 0:
        incremental = False

    logger.info("create new scan")
    scan = scan_api.create_new_scan(project_id=project_id, is_incremental=incremental)
    scan_id = scan.id
    logger.info("scan_id : {}".format(scan_id))

    logger.info("get scan details by scan id, report scan status")
    while True:
        scan_detail = scan_api.get_sast_scan_details_by_scan_id(scan_id=scan_id)
        scan_status = scan_detail.status.name
        logger.info("scan_status: {}".format(scan_status))
        if scan_status == "Finished":
            break
        elif scan_status == "Failed":
            return
        time.sleep(10)

    logger.info("get statistics results by scan id")
    statistics = scan_api.get_statistics_results_by_scan_id(scan_id=scan_id)
    statistics_updated = {
        "Critical": statistics.high_severity,
        "High": statistics.medium_severity,
        "Medium": statistics.low_severity,
        "Low": statistics.info_severity
    }
    logger.info(f"statistics: {statistics_updated}")
    return scan_id


def generate_report(scan_id: int, report_type: str, report_file_path: str):
    """

    Args:
        scan_id (int):
        report_type (str):
        report_file_path (str):

    Returns:

    """
    from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI
    scan_api = ScansAPI()

    logger.info("register scan report")
    report = scan_api.register_scan_report(scan_id=scan_id, report_type=report_type)
    report_id = report.report_id
    logger.info("report_id : {}".format(report_id))

    logger.info("get report status by id")
    while not scan_api.is_report_generation_finished(report_id):
        logger.info("report generating")
        time.sleep(10)

    logger.info("get report by id")
    report_content = scan_api.get_report_by_id(report_id)

    logger.info("write original report")
    with open(str(report_file_path), "wb") as f_out:
        f_out.write(report_content)

    if report_type.lower() == "csv":
        update_csv_report(cx_report_file_path=report_file_path, scan_id=scan_id)


def get_similarity_ids_of_a_scan(scan_id):
    from CheckmarxPythonSDK.CxODataApiSDK.HttpRequests import get_request
    url = f"/Cxwebinterface/odata/v1/Scans({scan_id})/Results?$select=SimilarityId,PathId"
    return get_request(relative_url=url)


def update_csv_report(cx_report_file_path, scan_id):
    """
    update CSV report by add the similarityID column (data retrieved by using ODATA API)
    Args:
        cx_report_file_path:
        scan_id:

    Returns:

    """
    logger.info("update csv report")
    if not pathlib.Path(cx_report_file_path).exists():
        logger.info(f"report does not exist, file path: {cx_report_file_path}")
        return
    import csv
    from collections import OrderedDict
    logger.info("get similarity id by using ODATA API")
    similarity_id_path_ids = get_similarity_ids_of_a_scan(scan_id=scan_id)
    sim_path_dict = {}
    for pair in similarity_id_path_ids:
        sim_path_dict[pair.get("PathId")] = pair.get("SimilarityId")

    logger.info("read csv file")
    csv_content = []
    with open(cx_report_file_path, newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        field_names = reader.fieldnames
        field_names = [item for item in field_names]
        field_names.append('SimilarityID')
        for row in reader:
            path_id = row.get("Link").split('&')[2].split('=')[1]
            path_id = int(path_id)
            similarity_id = sim_path_dict.get(path_id)
            new_ordered_dict = OrderedDict()
            for key, value in row.items():
                new_ordered_dict[key] = value
            new_ordered_dict['SimilarityID'] = similarity_id
            csv_content.append(new_ordered_dict)
    logger.info("write csv file")
    with open(cx_report_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, dialect='unix')
        writer.writeheader()
        writer.writerows(csv_content)


def run_scan_and_generate_reports(arguments):
    preset = arguments.preset
    incremental = False if arguments.incremental.lower() == "false" else True
    location_type = arguments.location_type
    location_path = arguments.location_path
    project_full_path = arguments.project_name
    exclude_folders = arguments.exclude_folders
    exclude_files = arguments.exclude_files
    report_xml = arguments.report_xml
    report_pdf = arguments.report_pdf
    report_csv = arguments.report_csv
    full_scan_cycle = int(arguments.full_scan_cycle)
    logger.info(
        f"preset: {preset}\n"
        f"incremental: {incremental}\n"
        f"location_type: {location_type}\n"
        f"location_path: {location_path}\n"
        f"project_name: {project_full_path}\n"
        f"report_xml: {report_xml}\n"
        f"report_pdf: {report_pdf}\n"
        f"report_csv: {report_csv}\n"
        f"full_scan_cycle: {full_scan_cycle}\n"
    )

    logger.info(f"creating zip file by zip the source code folder: {location_path}")
    project_path_list = project_full_path.split("/")
    project_name = project_path_list[-1]
    team_full_name = "/".join(project_path_list[0: len(project_path_list)-1])
    zip_file_path = create_zip_file_from_location_path(location_path, project_name)
    logger.info(f"ZIP file created: {zip_file_path}")
    scan_id = cx_scan_from_local_zip_file(preset_name=preset, team_full_name=team_full_name, project_name=project_name,
                                          zip_file_path=zip_file_path, exclude_folders=exclude_folders,
                                          exclude_files=exclude_files, incremental=incremental,
                                          full_scan_cycle=full_scan_cycle)

    logger.info(f"deleting zip file: {zip_file_path}")
    pathlib.Path(zip_file_path).unlink()

    if report_xml:
        generate_report(scan_id=scan_id, report_type="XML", report_file_path=report_xml)
    if report_pdf:
        generate_report(scan_id=scan_id, report_type="PDF", report_file_path=report_pdf)
    if report_csv:
        generate_report(scan_id=scan_id, report_type="CSV", report_file_path=report_csv)
    logger.info("report generated successfully")


if __name__ == '__main__':
    # get command line arguments
    cli_arguments = get_command_line_arguments()
    cli_arguments = cli_arguments[0]
    run_scan_and_generate_reports(cli_arguments)
