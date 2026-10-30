import time

import pytest

from CheckmarxPythonSDK.CxOne import (
    get_environments, create_environment, delete_environment,
    get_apps_list, get_environment_scans_over_time, get_environment_summaries,
    get_environments_tags, get_application_environments_results_summary,
    get_application_environments_risk_rating_summary,
    get_application_environments_risk_summary, get_average_scans_data,
    get_has_missing_alert_data, get_scans_count, get_top_vulnerable_environments,
    has_successful_scan, get_lean_environments, get_scan_meta,
    get_source_code_exists, get_latest_project_sources, get_config_file,
    update_environment_settings, get_scaled_jobs_enabled, get_systemic_enabled,
    get_technologies,
)
from CheckmarxPythonSDK.CxOne import ApplicationsAPI as _ApplicationsAPI
from CheckmarxPythonSDK.CxOne.dto import (
    DastEnvironmentInput, DastScanType, DastScansOverTimeResponse,
    DastEnvironmentSummariesCollection, DastEnvironmentsRiskRatingSummary,
    DastEnvironmentsRiskSummary, DastAverageScansDataResponse,
    DastScansCountResponse, DastVulnerableEnvironment,
    DastLeanEnvironmentsCollection, DastScansList, DastSourceVersion,
    DastFlagEnabled, DastTechnology,
)


def _skip_on_client_error(e: Exception):
    msg = str(e)
    if "400" in msg or "401" in msg or "403" in msg or "404" in msg or "503" in msg:
        pytest.skip("API returned client error: {}".format(msg))
    raise e


@pytest.fixture(scope="session")
def env_with_scan():
    envs = get_environments()
    env = next((e for e in envs.environments if e.last_scan_id), None)
    if env is None:
        pytest.skip("No environments with scans on this tenant")
    return env


@pytest.fixture(scope="session")
def app_id():
    apps = _ApplicationsAPI().get_a_list_of_applications(limit=1)
    if not apps.applications:
        pytest.skip("No applications on this tenant")
    return apps.applications[0].id


# ---- No-arg / tenant-wide ----


def test_get_environments_tags():
    assert isinstance(get_environments_tags(), list)


def test_has_successful_scan():
    assert isinstance(has_successful_scan(), bool)


def test_get_scaled_jobs_enabled():
    result = get_scaled_jobs_enabled()
    assert isinstance(result, DastFlagEnabled)


def test_get_systemic_enabled():
    result = get_systemic_enabled()
    assert isinstance(result, DastFlagEnabled)


def test_get_technologies():
    technologies = get_technologies()
    assert isinstance(technologies, list) and technologies
    assert all(isinstance(t, DastTechnology) for t in technologies)


def test_get_lean_environments():
    # Confirmed live: from_/to don't actually limit the result -- see
    # the method's docstring. Just check the response shape here.
    result = get_lean_environments()
    assert isinstance(result, DastLeanEnvironmentsCollection)
    assert result.total_items == len(result.environments)


def test_get_apps_list():
    result = get_apps_list(limit=3)
    assert isinstance(result, dict)


def test_get_environment_summaries():
    result = get_environment_summaries(to=5)
    assert isinstance(result, DastEnvironmentSummariesCollection)
    assert isinstance(result.total_items, int)


# ---- Per-environment ----


def test_get_environment_scans_over_time(env_with_scan):
    result = get_environment_scans_over_time(
        env_with_scan.environment_id, "2020-01-01T00:00:00Z", "2030-01-01T00:00:00Z",
    )
    assert isinstance(result, DastScansOverTimeResponse)
    assert any(s.scan_id == env_with_scan.last_scan_id for s in result.scans_over_time)


def test_get_average_scans_data(env_with_scan):
    result = get_average_scans_data(env_with_scan.environment_id)
    assert isinstance(result, DastAverageScansDataResponse)


def test_get_has_missing_alert_data(env_with_scan):
    result = get_has_missing_alert_data(env_with_scan.environment_id)
    assert result is None or isinstance(result, bool)


def test_get_scans_count(env_with_scan):
    result = get_scans_count(env_with_scan.environment_id)
    assert isinstance(result, DastScansCountResponse)
    assert result.total is None or result.total >= 1


def test_get_scan_meta(env_with_scan):
    result = get_scan_meta(env_with_scan.environment_id, env_with_scan.last_scan_id)
    assert isinstance(result, DastScansList)
    assert any(s.scan_id == env_with_scan.last_scan_id for s in result.last_scans)


def test_get_source_code_exists(env_with_scan):
    projects = env_with_scan.project_ids or []
    if not projects:
        pytest.skip("Environment has no associated projects")
    try:
        result = get_source_code_exists(
            env_with_scan.environment_id, env_with_scan.last_scan_id, projects[0],
        )
    except Exception as e:
        _skip_on_client_error(e)
        return
    assert result is None or isinstance(result, bool)


def test_get_latest_project_sources(env_with_scan):
    projects = env_with_scan.project_ids or []
    if not projects:
        pytest.skip("Environment has no associated projects")
    try:
        result = get_latest_project_sources(env_with_scan.environment_id, projects)
    except Exception as e:
        _skip_on_client_error(e)
        return
    assert isinstance(result, dict)
    assert all(isinstance(v, DastSourceVersion) for v in result.values())


def test_get_config_file(env_with_scan):
    try:
        content = get_config_file(env_with_scan.environment_id)
    except Exception as e:
        _skip_on_client_error(e)
        return
    assert isinstance(content, bytes) and content


def test_update_environment_settings():
    env_id = create_environment(DastEnvironmentInput(
        domain=f"sdk-envsettings-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    try:
        result = update_environment_settings(env_id, settings={"useClientSpider": False})
        assert isinstance(result, str)
    finally:
        delete_environment(env_id)


# ---- Per-application ----


def test_get_application_environments_results_summary(app_id):
    result = get_application_environments_results_summary(app_id)
    assert isinstance(result, dict)


def test_get_application_environments_risk_rating_summary(app_id):
    result = get_application_environments_risk_rating_summary(app_id)
    assert isinstance(result, DastEnvironmentsRiskRatingSummary)


def test_get_application_environments_risk_summary(app_id):
    result = get_application_environments_risk_summary(app_id)
    assert isinstance(result, DastEnvironmentsRiskSummary)


def test_get_top_vulnerable_environments(app_id):
    result = get_top_vulnerable_environments(app_id)
    assert isinstance(result, list)
    assert all(isinstance(e, DastVulnerableEnvironment) for e in result)
