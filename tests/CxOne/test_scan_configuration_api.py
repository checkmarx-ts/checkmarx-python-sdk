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


def test_get_the_list_of_all_the_parameters_defined_for_the_current_tenant():
    scan_parameters = get_the_list_of_all_the_parameters_defined_for_the_current_tenant()
    assert scan_parameters is not None


def test_define_parameters_in_the_input_list_for_the_current_tenant():
    scan_parameters = []
    is_successful = define_parameters_in_the_input_list_for_the_current_tenant(scan_parameters=scan_parameters)
    assert is_successful is True


def test_get_the_list_of_all_the_parameters_for_a_project():
    project_id = "58b051e7-8c1f-437d-bbf1-d25800bd57f1"
    scan_parameters = get_the_list_of_all_the_parameters_for_a_project(project_id=project_id)
    assert scan_parameters is not None


def test_define_parameters_in_the_input_list_for_a_specific_project():
    project_id = "58b051e7-8c1f-437d-bbf1-d25800bd57f1"
    scan_parameters = [
        ScanParameter(
            key="scan.handler.git.repository",
            name="repository",
            category="git",
            origin_level="Project",
            value="https://github.com/WebGoat/WebGoat.git",
            value_type="String",
            value_type_params=None,
            allow_override=True
        )
    ]
    is_successful = define_parameters_in_the_input_list_for_a_specific_project(
        project_id=project_id,
        scan_parameters=scan_parameters
    )
    assert is_successful is True


def test_get_the_list_of_all_parameters_that_will_be_used_in_the_scan_run():
    project_id = "58b051e7-8c1f-437d-bbf1-d25800bd57f1"
    scan_id = "5b7e4dcc-2add-49e4-91c0-603a6c08cd55"
    scan_parameters = get_the_list_of_all_parameters_that_will_be_used_in_the_scan_run(
        project_id=project_id, scan_id=scan_id
    )
    assert scan_parameters is not None


def test_get_all_default_configs_for_the_tenant():
    all_configs = get_all_default_configs_for_the_tenant()
    assert all_configs is not None


def test_create_a_default_config_for_the_sast_engine():
    default_config = DefaultConfig()
    create_a_default_config_for_the_sast_engine(default_config=default_config)


def test_get_sast_default_config_by_id():
    config_id = ""
    config = get_sast_default_config_by_id(config_id=config_id)
    assert config is not None


def test_update_default_config_for_the_sast_engine():
    config_id = ""
    default_config = DefaultConfig()
    is_successful = update_default_config_for_the_sast_engine(config_id=config_id, default_config=default_config)
    assert is_successful is True


def test_delete_a_sast_default_config():
    config_id = ""
    is_successful = delete_a_sast_default_config(config_id=config_id)
    assert is_successful is True
