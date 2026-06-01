import os
import tempfile
import time

import pytest

from CheckmarxPythonSDK.CxOne import (
    get_tenant_overview, get_environments, create_environment,
    update_environment, get_environment_by_id, delete_environment,
    get_environments_count_by_group, run_scan, run_public_scan, update_scan,
    dast_cancel_scan, dast_delete_scan, get_scans, get_scans_count_by_group,
    dast_get_scan_by_id, get_scan_log,
)
from CheckmarxPythonSDK.CxOne.dto import (
    TenantOverview, DastEnvironmentsCollection, DastEnvironment,
    DastEnvironmentFilter, DastLastRiskRating, DastAuthSuccess, DastTunnelState,
    DastSortBy, DastAlertRiskLevel, DastApplication, DastScanConfig,
    DastEnvironmentInput, DastEnvironmentSettings, DastCliSettings, DastAuthSettings,
    DastTotpField, DastConfigFileSettings, DastCustomHeader,
    DastSessionManagementHeader, DastScanOptions, DastScanOption,
    DastEnvironmentUpdate, DastAutomationScript, DastAutomationType,
    DastAutomationAction, DastAutomationScriptType, DastAutomationEngine,
    DastScanType, DastGroupBy, DastEnvironmentGroupCount,
    DastRunScanInput, DastScanUpdate,
    DastScansCollection, DastScan, DastScanFilter, DastScanSortBy, DastScanStatus,
    DastScanGroupBy, DastScanGroupCount,
)


def test_get_tenant_overview():
    overview = get_tenant_overview()
    assert isinstance(overview, TenantOverview)
    assert overview.tenant_id is not None
    assert overview.environments_count is not None
    assert overview.risk_rating is not None


def test_get_environments():
    collection = get_environments(to=5)
    assert isinstance(collection, DastEnvironmentsCollection)
    assert collection.total_items is not None
    assert isinstance(collection.environments, list)
    if collection.environments:
        env = collection.environments[0]
        assert isinstance(env, DastEnvironment)
        assert env.environment_id is not None
        # Nested DTO typing
        assert env.scan_config is None or isinstance(env.scan_config, DastScanConfig)
        assert isinstance(env.applications, list)
        assert all(isinstance(a, DastApplication) for a in env.applications)
        assert env.alert_risk_level is None or isinstance(env.alert_risk_level, DastAlertRiskLevel)


def test_dast_environment_filter_to_dict():
    f = DastEnvironmentFilter(
        domain="example.com",
        last_risk_rating=DastLastRiskRating.HIGH,
        auth_success=DastAuthSuccess.NO_AUTH,
        tunnel_state=DastTunnelState.CONNECTED,
    )
    assert f.to_dict() == {
        "domain": "example.com",
        "lastRiskRating": "High",
        "authSuccess": "no_auth",
        "tunnelState": "connected",
    }


def test_get_environments_with_filter_dto():
    f = DastEnvironmentFilter(scan_type=DastScanType.DAST)
    collection = get_environments(filter_=f, to=5)
    assert isinstance(collection, DastEnvironmentsCollection)
    for env in collection.environments:
        # _coerce_scan_type maps the wire "DAST" to the enum member;
        # equality works either way because StrEnum compares with strings.
        assert env.scan_type == DastScanType.DAST or env.scan_type == "DAST"


def test_dast_sort_by_enum_values():
    assert DastSortBy.CREATED.value == "created"
    assert DastSortBy.SCAN_TYPE.value == "scantype"


def test_get_environments_with_sort():
    # Enum entry → defaults to :asc
    asc = get_environments(sort=[DastSortBy.CREATED])
    # Raw "<col>:desc" string escape-hatch in the same list
    desc = get_environments(sort=["created:desc"])
    if len(asc.environments) >= 2 and len(desc.environments) >= 2:
        assert asc.environments[0].created <= asc.environments[-1].created
        assert desc.environments[0].created >= desc.environments[-1].created
        # asc and desc should reverse the relative order of the extremes
        assert asc.environments[0].environment_id == desc.environments[-1].environment_id


def test_dast_environment_input_to_dict():
    inp = DastEnvironmentInput(
        domain="example.com",
        url="https://example.com",
        scan_type=DastScanType.DAST,
        project_ids=["project-uuid"],
        tags=["production"],
        is_public=False,
        has_auth=True,
        settings=DastEnvironmentSettings(
            cli_settings=DastCliSettings(output="/tmp/out", retry=3, retry_delay=5000, update_interval=10000),
            auth_settings=DastAuthSettings(
                verification_url="https://example.com/verify",
                logged_in_regex="Welcome.*",
                login_page_wait=2000,
                include_paths=["https://example.com/api/.*"],
            ),
        ),
    )
    assert inp.to_dict() == {
        "domain": "example.com",
        "url": "https://example.com",
        "scanType": "DAST",
        "projectIds": ["project-uuid"],
        "tags": ["production"],
        "isPublic": False,
        "hasAuth": True,
        "settings": {
            "cliSettings": {
                "output": "/tmp/out", "retry": 3,
                "retryDelay": 5000, "updateInterval": 10000,
            },
            "authSettings": {
                "verificationUrl": "https://example.com/verify",
                "loggedInRegex": "Welcome.*",
                "loginPageWait": 2000,
                "includePaths": ["https://example.com/api/.*"],
            },
        },
    }


def test_dast_environment_settings_full_shape():
    """Exercise every nested DTO under settings to lock down the wire keys."""
    s = DastEnvironmentSettings(
        cli_settings=DastCliSettings(jvm_properties="-Xmx2g", log_level="DEBUG"),
        auth_settings=DastAuthSettings(
            logged_out_regex="Please log in",
            poll_post_data="user=x",
            totp_field=DastTotpField(attribute="name", value="otp"),
            poll_additional_headers="X-Foo: bar",
        ),
        config_file_settings=DastConfigFileSettings(exclude_paths=["/admin/.*"]),
        custom_headers=[DastCustomHeader(header="X-API", value="123", url="https://example.com/api/.*")],
        session_management=[DastSessionManagementHeader(header="Cookie", value="sid=abc")],
        scan_options=DastScanOptions(
            scan_option=DastScanOption.DEEP,
            include_server=True,
            slow_app=False,
        ),
    )
    assert s.to_dict() == {
        "cliSettings": {"jvmProperties": "-Xmx2g", "logLevel": "DEBUG"},
        "authSettings": {
            "loggedOutRegex": "Please log in",
            "pollPostData": "user=x",
            "totpField": {"attribute": "name", "value": "otp"},
            "pollAdditionalHeaders": "X-Foo: bar",
        },
        "configFileSettings": {"excludePaths": ["/admin/.*"]},
        "customHeaders": [{"header": "X-API", "value": "123", "url": "https://example.com/api/.*"}],
        "sessionManagement": [{"header": "Cookie", "value": "sid=abc"}],
        "scanOptions": {"scanOption": "deep", "includeServer": True, "slowApp": False},
    }


def test_create_environment():
    # Minimal create — domain/url/scan_type are the required fields.
    inp = DastEnvironmentInput(
        domain=f"sdk-test-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    )
    env_id = create_environment(inp)
    try:
        assert isinstance(env_id, str) and env_id
        # Should look like a UUID (36 chars with dashes), not the raw API endpoint
        assert len(env_id) == 36 and env_id.count("-") == 4
    finally:
        delete_environment(env_id)


def test_dast_environment_update_to_dict():
    upd = DastEnvironmentUpdate(
        environment_id="uuid",
        domain="example.com",
        tags=["production", "updated"],
        app_ids=["app-uuid"],
        primary_app_ids=["primary-app-uuid"],
        tunnel_id="tunnel-uuid",
        settings=DastEnvironmentSettings(
            automation_scripts=[
                DastAutomationScript(
                    type=DastAutomationType.SCRIPT,
                    action=DastAutomationAction.ADD,
                    script_type=DastAutomationScriptType.HTTP_SENDER,
                    inline="logger.info('hello');",
                    engine=DastAutomationEngine.ECMASCRIPT_GRAALJS,
                    name="my-script",
                ),
            ],
        ),
    )
    assert upd.to_dict() == {
        "environmentId": "uuid",
        "domain": "example.com",
        "tags": ["production", "updated"],
        "appIds": ["app-uuid"],
        "primaryAppIds": ["primary-app-uuid"],
        "tunnelId": "tunnel-uuid",
        "settings": {
            "automationScripts": [{
                "type": "script",
                "action": "add",
                "scriptType": "httpsender",
                "inline": "logger.info('hello');",
                "engine": "ECMAScript : Graal.js",
                "name": "my-script",
            }],
        },
    }


def test_update_environment():
    # Create a throwaway env, update its domain, then verify the change.
    original = f"sdk-update-{int(time.time())}"
    env_id = create_environment(DastEnvironmentInput(
        domain=original,
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    try:
        new_domain = original + "-renamed"
        ok = update_environment(DastEnvironmentUpdate(
            environment_id=env_id,
            domain=new_domain,
        ))
        assert ok is True
        refreshed = get_environment_by_id(env_id)
        assert isinstance(refreshed, DastEnvironment)
        assert refreshed.domain == new_domain
    finally:
        delete_environment(env_id)


def test_get_environment_by_id():
    domain = f"sdk-get-{int(time.time())}"
    env_id = create_environment(DastEnvironmentInput(
        domain=domain,
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    try:
        env = get_environment_by_id(env_id)
        assert isinstance(env, DastEnvironment)
        assert env.environment_id == env_id
        assert env.domain == domain
        assert env.scan_type == DastScanType.DAST or env.scan_type == "DAST"
    finally:
        delete_environment(env_id)


def test_get_environments_count_by_group():
    buckets = get_environments_count_by_group(group_by=[DastGroupBy.SCAN_TYPE])
    assert isinstance(buckets, list)
    assert all(isinstance(b, DastEnvironmentGroupCount) for b in buckets)
    # When grouping by scan_type, the sum of itemCount should equal the total
    # environments_count from the tenant overview.
    total = sum(b.item_count or 0 for b in buckets)
    overview = get_tenant_overview()
    assert total == overview.environments_count
    # Each bucket's `groups` is a list with one entry (the scan type value)
    assert all(b.groups and len(b.groups) == 1 for b in buckets)


def test_run_scan():
    # Create a throwaway env to scan against.
    env_id = create_environment(DastEnvironmentInput(
        domain=f"sdk-runscan-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    config_path = tempfile.NamedTemporaryFile(suffix=".yaml", delete=False).name
    with open(config_path, "w") as f:
        # Minimal ZAP automation YAML. The scan itself may fail downstream,
        # but the API accepts this shape and returns a scan id.
        f.write("---\nenv:\n  contexts:\n    - name: dummy\n")
    try:
        scan_id = run_scan(DastRunScanInput(
            environment_id=env_id,
            scan_type=DastScanType.DAST,
            configuration_file=config_path,
        ))
        assert isinstance(scan_id, str) and len(scan_id) == 36 and scan_id.count("-") == 4
    finally:
        os.unlink(config_path)
        delete_environment(env_id)


def test_dast_scan_update_to_dict():
    upd = DastScanUpdate(
        scan_id="scan-uuid",
        environment_id="env-uuid",
        scan_type=DastScanType.DAST,
        tags=["a", "b"],
        groups=["c", "d"],
    )
    assert upd.to_dict() == {
        "scanId": "scan-uuid",
        "environmentID": "env-uuid",
        "scanType": "DAST",
        "tags": ["a", "b"],
        "groups": ["c", "d"],
    }


def test_update_scan():
    # Create env → run scan → update the scan's tags → verify no error.
    env_id = create_environment(DastEnvironmentInput(
        domain=f"sdk-upscan-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    config_path = tempfile.NamedTemporaryFile(suffix=".yaml", delete=False).name
    with open(config_path, "w") as f:
        f.write("---\nenv:\n  contexts:\n    - name: dummy\n")
    try:
        scan_id = run_scan(DastRunScanInput(
            environment_id=env_id,
            scan_type=DastScanType.DAST,
            configuration_file=config_path,
        ))
        result = update_scan(DastScanUpdate(
            scan_id=scan_id,
            environment_id=env_id,
            # Spec says scan_type is optional but the live API rejects
            # without it with "ScanType oneof DAST DASTAPI".
            scan_type=DastScanType.DAST,
            tags=["sdk-test-updated"],
        ))
        # Response is a string body (per spec); 2xx is what matters.
        # check_response would have raised on non-2xx.
        assert isinstance(result, str)
    finally:
        os.unlink(config_path)
        delete_environment(env_id)


def test_cancel_scan():
    env_id = create_environment(DastEnvironmentInput(
        domain=f"sdk-cancel-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    config_path = tempfile.NamedTemporaryFile(suffix=".yaml", delete=False).name
    with open(config_path, "w") as f:
        f.write("---\nenv:\n  contexts:\n    - name: dummy\n")
    try:
        scan_id = run_scan(DastRunScanInput(
            environment_id=env_id,
            scan_type=DastScanType.DAST,
            configuration_file=config_path,
        ))
        ok = dast_cancel_scan(scan_id=scan_id, environment_id=env_id)
        assert ok is True
    finally:
        os.unlink(config_path)
        delete_environment(env_id)


def test_delete_scan():
    env_id = create_environment(DastEnvironmentInput(
        domain=f"sdk-delscan-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    config_path = tempfile.NamedTemporaryFile(suffix=".yaml", delete=False).name
    with open(config_path, "w") as f:
        f.write("---\nenv:\n  contexts:\n    - name: dummy\n")
    try:
        scan_id = run_scan(DastRunScanInput(
            environment_id=env_id,
            scan_type=DastScanType.DAST,
            configuration_file=config_path,
        ))
        # Cancel before delete — the API rejects deleting a running scan
        # in some cases (saw this in CxSAST too).
        dast_cancel_scan(scan_id=scan_id, environment_id=env_id)
        ok = dast_delete_scan(scan_id=scan_id, environment_id=env_id)
        assert ok is True
    finally:
        os.unlink(config_path)
        delete_environment(env_id)


def test_get_scans():
    # Find an env that already has at least one scan so we can verify
    # the response is non-empty.
    envs = get_environments()
    env_with_scan = next((e for e in envs.environments if e.last_scan_id), None)
    if env_with_scan is None:
        pytest.skip("no environments have scans on this tenant")
    collection = get_scans(environment_id=env_with_scan.environment_id, to=3)
    assert isinstance(collection, DastScansCollection)
    assert collection.total_scans is not None and collection.total_scans >= 1
    assert isinstance(collection.scans, list) and collection.scans
    s = collection.scans[0]
    assert isinstance(s, DastScan)
    assert s.scan_id is not None
    # NOTE: the live API returns an empty string for `environmentId` on
    # the scan object rather than echoing the queried env. environment_id
    # is parsed correctly — just don't expect it to match.


def test_get_scan_log():
    envs = get_environments()
    env_with_scan = next(
        (e for e in envs.environments if e.last_scan_id and e.has_report),
        None,
    )
    if env_with_scan is None:
        # Fall back to any env with a scan; the API may still return a log.
        env_with_scan = next((e for e in envs.environments if e.last_scan_id), None)
    if env_with_scan is None:
        pytest.skip("no environments have scans on this tenant")
    archive = get_scan_log(scan_id=env_with_scan.last_scan_id)
    assert isinstance(archive, bytes)
    # ZIP files start with the "PK" magic bytes
    assert archive[:2] == b"PK", f"expected ZIP magic, got {archive[:8]!r}"


def test_dast_get_scan_by_id():
    envs = get_environments()
    env_with_scan = next((e for e in envs.environments if e.last_scan_id), None)
    if env_with_scan is None:
        pytest.skip("no environments have scans on this tenant")
    scan = dast_get_scan_by_id(scan_id=env_with_scan.last_scan_id)
    assert isinstance(scan, DastScan)
    assert scan.scan_id == env_with_scan.last_scan_id


def test_get_scans_count_by_group():
    envs = get_environments()
    env_with_scan = next((e for e in envs.environments if e.last_scan_id), None)
    if env_with_scan is None:
        pytest.skip("no environments have scans on this tenant")
    buckets = get_scans_count_by_group(
        environment_id=env_with_scan.environment_id,
        group_by=[DastScanGroupBy.INITIATOR],
    )
    assert isinstance(buckets, list)
    assert all(isinstance(b, DastScanGroupCount) for b in buckets)
    assert buckets, "expected at least one bucket on an env that has scans"


@pytest.mark.skip(
    reason="Requires an Environment fully configured via the UI's DAST "
           "Environment Setup Wizard (with a working auth session). "
           "Bare API-created envs return HTTP 400 'failed to get auth session'."
)
def test_run_public_scan():
    env_id = create_environment(DastEnvironmentInput(
        domain=f"sdk-public-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    try:
        scan_id = run_public_scan(environment_id=env_id)
        assert isinstance(scan_id, str) and len(scan_id) == 36
        try:
            dast_cancel_scan(scan_id=scan_id, environment_id=env_id)
            dast_delete_scan(scan_id=scan_id, environment_id=env_id)
        except Exception:
            pass
    finally:
        delete_environment(env_id)


def test_delete_environment():
    env_id = create_environment(DastEnvironmentInput(
        domain=f"sdk-delete-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    ok = delete_environment(env_id)
    assert ok is True
    # Subsequent GET should fail — the env no longer exists.
    with pytest.raises(Exception):
        get_environment_by_id(env_id)
