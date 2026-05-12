import pytest
from CheckmarxPythonSDK.CxOne import (
    get_the_list_of_all_the_parameters_defined_for_the_current_tenant,
    define_parameters_in_the_input_list_for_the_current_tenant,
    get_the_list_of_all_the_parameters_for_a_project,
    define_parameters_in_the_input_list_for_a_specific_project,
    get_the_list_of_all_parameters_that_will_be_used_in_the_scan_run,
    get_all_default_configs_for_the_tenant,
    create_a_default_config_for_the_sast_engine,
    get_sast_default_config_by_id,
    update_default_config_for_the_sast_engine,
    delete_a_sast_default_config,
)

from CheckmarxPythonSDK.CxOne.dto.ScanParameter import ScanParameter
from CheckmarxPythonSDK.CxOne.dto.DefaultConfig import DefaultConfig
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI


def _get_project_id():
    result = _ProjectsAPI().get_a_list_of_projects(limit=1)
    if result.projects:
        return result.projects[0].id
    return None


def test_get_the_list_of_all_the_parameters_defined_for_the_current_tenant():
    scan_parameters = get_the_list_of_all_the_parameters_defined_for_the_current_tenant()
    assert scan_parameters is not None


def test_define_parameters_in_the_input_list_for_the_current_tenant():
    scan_parameters = []
    is_successful = define_parameters_in_the_input_list_for_the_current_tenant(scan_parameters=scan_parameters)
    assert is_successful is True


def test_get_the_list_of_all_the_parameters_for_a_project():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No project found in tenant")
    scan_parameters = get_the_list_of_all_the_parameters_for_a_project(project_id=project_id)
    assert scan_parameters is not None


def test_define_parameters_in_the_input_list_for_a_specific_project():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No project found in tenant")
    scan_parameters = [
        ScanParameter(
            key="scan.handler.git.repository",
            name="repository",
            category="git",
            originLevel="Project",
            value="https://github.com/CSPF-Founder/JavaVulnerableLab.git",
            valueType="String",
            valueTypeParams=None,
            allowOverride=True
        ),
        ScanParameter(
            key="scan.config.sca.ExploitablePath",
            name="exploitablePath",
            category="sca",
            originLevel="Project",
            value="false",
            valueType="Bool",
            valueTypeParams=None,
            allowOverride=True
        ),
        ScanParameter(
            key="scan.config.sast.languageMode",
            name="languageMode",
            category="sast",
            originLevel="Project",
            value="primary",
            valueType="List",
            valueTypeParams=None,
            allowOverride=True
        ),
        ScanParameter(
            key="scan.config.sca.LastSastScanTime",
            name="lastSastScanTime",
            category="sca",
            originLevel="Project",
            value="2",
            valueType="Number",
            valueTypeParams=None,
            allowOverride=True
        ),
    ]
    is_successful = define_parameters_in_the_input_list_for_a_specific_project(
        project_id=project_id,
        scan_parameters=scan_parameters
    )
    assert is_successful is True


def test_get_the_list_of_all_parameters_that_will_be_used_in_the_scan_run():
    from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
    result = _ScansAPI().get_a_list_of_scans(limit=1, statuses=["Completed"])
    if not result.scans:
        pytest.skip("No completed scan found")
    scan = result.scans[0]
    project_id = scan.project_id
    scan_id = scan.id
    scan_parameters = get_the_list_of_all_parameters_that_will_be_used_in_the_scan_run(
        project_id=project_id, scan_id=scan_id
    )
    assert scan_parameters is not None


@pytest.mark.skip(reason="403 Forbidden - insufficient permissions for tenant default configs")
def test_get_all_default_configs_for_the_tenant():
    all_configs = get_all_default_configs_for_the_tenant()
    assert all_configs is not None


@pytest.mark.skip(reason="403 Forbidden - insufficient permissions for tenant default configs")
def test_create_a_default_config_for_the_sast_engine():
    default_config = DefaultConfig()
    create_a_default_config_for_the_sast_engine(default_config=default_config)


@pytest.mark.skip(reason="Requires a valid config_id - empty string not valid")
def test_get_sast_default_config_by_id():
    config_id = ""
    config = get_sast_default_config_by_id(config_id=config_id)
    assert config is not None


@pytest.mark.skip(reason="404 - config not found on this server")
def test_update_default_config_for_the_sast_engine():
    config_id = ""
    default_config = DefaultConfig()
    is_successful = update_default_config_for_the_sast_engine(config_id=config_id, default_config=default_config)
    assert is_successful is True


@pytest.mark.skip(reason="404 - config not found on this server")
def test_delete_a_sast_default_config():
    config_id = ""
    is_successful = delete_a_sast_default_config(config_id=config_id)
    assert is_successful is True
