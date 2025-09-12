import time

from CheckmarxPythonSDK.CxOne import (
    create_a_project,
    create_scan,
    create_a_pre_signed_url_to_upload_files,
    upload_zip_content_for_scanning,
    get_project_id_by_name,
    get_a_list_of_scans,
    get_all_scan_tags,
    get_summary_of_the_status_of_the_scans,
    get_the_list_of_available_config_as_code_template_files,
    get_the_config_as_code_template_file,
    get_scan_by_id,
    cancel_scan,
    delete_scan,
    get_a_detailed_workflow_of_a_scan,
    get_a_list_of_scan,
    get_scans_by_filters,
)

from CheckmarxPythonSDK.CxOne.dto import (
    Upload,
    Git,
    Project,
    ScanConfig,
    ScanInput,
    ProjectInput,
)

new_project_name = "happy-cook/JavaVulnerableLab"


def test_ast_create_scan_by_upload_file():
    project_id = get_project_id_by_name(name=new_project_name)
    if not project_id:
        project = create_a_project(ProjectInput(name=new_project_name))
        project_id = project.id
    url = create_a_pre_signed_url_to_upload_files()
    is_successful = upload_zip_content_for_scanning(
        upload_link=url,
        zip_file_path=("/home/happy/Documents/software/application_security/checkmarx/tools/checkmarx-python-sdk"
                       "/tests/JavaVulnerableLab-master.zip")
    )
    assert is_successful is True
    scan_input = ScanInput(
        scan_type="upload",
        handler=Upload(upload_url=url, branch="master"),
        project=Project(project_id=project_id, tags={"test": "", "priority": "high"}),
        configs=[
            ScanConfig("sast", {"incremental": "false", "presetName": "ASA Premium"}),
            ScanConfig("sca"),
            ScanConfig("kics")
        ],
        tags={
            "test": "",
            "scan_tag": "happy"
        }
    )
    scan = create_scan(scan_input=scan_input)
    scan_id = scan.id
    assert scan_id is not None


def test_get_a_list_of_scan():
    project_id = get_project_id_by_name(name=new_project_name)
    scans_collection = get_a_list_of_scans(project_id=project_id, branch='master', limit=1, sort=["-created_at"])
    assert len(scans_collection.scans) > 0


def test_get_all_scan_tags():
    scan_tags = get_all_scan_tags()
    assert scan_tags is not None


def test_get_summary_of_the_status_of_the_scans():
    scan_summary = get_summary_of_the_status_of_the_scans()
    assert scan_summary is not None


def test_get_the_list_of_available_config_as_code_template_files():
    templates = get_the_list_of_available_config_as_code_template_files()
    assert templates is not None


def test_get_the_config_as_code_template_file():
    template = get_the_config_as_code_template_file(file_name="config")
    assert template is not None


def test_get_scan_by_id():
    project_id = get_project_id_by_name(name=new_project_name)
    scans_collection = get_a_list_of_scan(project_id=project_id)
    scan_id = scans_collection.scans[0].id
    scan = get_scan_by_id(scan_id=scan_id)
    assert scan is not None


def test_get_a_detailed_workflow_of_a_scan():
    project_id = get_project_id_by_name(name=new_project_name)
    scans_collection = get_a_list_of_scan(project_id=project_id)
    scan_id = scans_collection.scans[0].id
    work_flows = get_a_detailed_workflow_of_a_scan(scan_id=scan_id)
    assert work_flows is not None


def test_ast_create_scan_by_git():
    project_id = get_project_id_by_name(name=new_project_name)
    if not project_id:
        project = create_a_project(ProjectInput(name=new_project_name))
        project_id = project.id
    scan_input = ScanInput(
        scan_type="git",
        handler=Git(
            repo_url="https://github.com/CSPF-Founder/JavaVulnerableLab.git",
            branch="master",
        ),
        project=Project(project_id=project_id),
        configs=[
            ScanConfig("sast", {"incremental": "false", "presetName": "ASA Premium"}),
            ScanConfig("sca"),
            ScanConfig("kics")
        ],
        tags={
            "test": "",
            "scan_tag": "happy"
        }
    )
    scan = create_scan(scan_input=scan_input)
    scan_id = scan.id
    assert scan_id is not None


def test_cancel_scan():
    project_id = get_project_id_by_name(name=new_project_name)
    scans_collection = get_a_list_of_scan(project_id=project_id, sort=["-created_at"])
    scan_id = scans_collection.scans[0].id
    is_successful = cancel_scan(scan_id=scan_id)
    assert is_successful is True


def test_delete_scan():
    project_id = get_project_id_by_name(name=new_project_name)
    scans_collection = get_a_list_of_scan(project_id=project_id)
    scan_id = scans_collection.scans[0].id
    time.sleep(60)
    is_successful = delete_scan(scan_id=scan_id)
    assert is_successful is True


def test_get_scans_by_filters():
    scans = get_scans_by_filters(search_id="", sort_by=["-created_at"])
    assert scans is not None
