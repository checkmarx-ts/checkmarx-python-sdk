import time

import pytest

from CheckmarxPythonSDK.CxOne import (
    create_environment, delete_environment,
    create_pipeline, update_pipeline, delete_pipeline,
    associate_apps_with_environment, associate_envs_with_application,
    get_associated_apps, get_associated_envs,
    disassociate_apps_from_environment, disassociate_envs_from_application,
)
from CheckmarxPythonSDK.CxOne import ApplicationsAPI as _ApplicationsAPI
from CheckmarxPythonSDK.CxOne.dto import (
    DastEnvironmentInput, DastScanType,
    DastApplicationEnvironmentWithPrimary, DastApplicationEnvironmentInfo,
)

_NIL_UUID = "00000000-0000-0000-0000-000000000000"


@pytest.fixture
def env_id():
    eid = create_environment(DastEnvironmentInput(
        domain=f"sdk-pipeline-appassoc-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    try:
        yield eid
    finally:
        delete_environment(eid)


@pytest.fixture(scope="session")
def app_id():
    apps = _ApplicationsAPI().get_a_list_of_applications(limit=1)
    if not apps.applications:
        pytest.skip("No applications on this tenant")
    return apps.applications[0].id


# ---- Pipeline ----


def test_pipeline_lifecycle(env_id):
    pipeline_id = create_pipeline(env_id)
    assert isinstance(pipeline_id, str) and pipeline_id

    result = update_pipeline(
        pipeline_id, env_id, current_step_type="scan", current_step_id=_NIL_UUID,
    )
    assert isinstance(result, str)

    result = delete_pipeline(pipeline_id, env_id)
    assert isinstance(result, str)


# ---- Application association ----


def test_associate_and_disassociate_apps_with_environment(env_id, app_id):
    assert associate_apps_with_environment(env_id, [app_id]) is True

    apps = get_associated_apps(env_id)
    assert isinstance(apps, list)
    assert any(
        isinstance(a, DastApplicationEnvironmentWithPrimary) and a.id == app_id
        for a in apps
    )

    assert disassociate_apps_from_environment(env_id, [app_id]) is True
    assert get_associated_apps(env_id) == []


def test_associate_and_disassociate_envs_with_application(env_id, app_id):
    assert associate_envs_with_application(app_id, [env_id], primary_environment_id=env_id) is True

    envs = get_associated_envs(app_id)
    assert isinstance(envs, list)
    matching = [e for e in envs if isinstance(e, DastApplicationEnvironmentInfo) and e.environment_id == env_id]
    assert len(matching) == 1
    assert matching[0].is_primary is True

    primary_only = get_associated_envs(app_id, primary=True)
    assert any(e.environment_id == env_id for e in primary_only)

    assert disassociate_envs_from_application(app_id, [env_id]) is True
    assert not any(e.environment_id == env_id for e in get_associated_envs(app_id))
