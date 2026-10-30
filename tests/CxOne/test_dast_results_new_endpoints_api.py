import pytest

from CheckmarxPythonSDK.CxOne import (
    get_environments, get_scans,
    health_check, get_alert_info, get_alert_instances, get_alert_level_results,
    post_alert_level_results, get_grouped_alert_level_results,
    post_grouped_alert_level_results, get_full_scan_results,
    get_vulnerability_summary, is_alert_level_enabled, get_aging_summary,
    get_instance_findings, get_top_five_risks, get_scan_sites_tree,
    get_results_states_summary, get_compliance_analytics,
    get_latest_correlation_results, get_compliance_over_time,
    get_occurrences_over_time, get_risk_level_over_time, get_states_over_time,
    get_manual_findings, create_manual_findings_batch, update_manual_finding_alert,
    get_manual_finding_alert_info, update_manual_finding_alert_instance,
    get_manual_findings_alert_level, get_grouped_manual_findings_alert_level,
    delete_manual_finding_alerts, get_grouped_manual_findings,
    update_manual_finding_instance, get_manual_finding_instance_info,
    get_manual_finding_instance_screenshots, unlink_manual_findings,
    delete_manual_finding_instances, get_instance_screenshots,
    upload_instance_screenshots, delete_instance_screenshots,
    get_pentest_findings, get_pentest_finding_details, get_pentest_wstg_coverage,
)
from CheckmarxPythonSDK.CxOne import ApplicationsAPI as _ApplicationsAPI
from CheckmarxPythonSDK.CxOne.dto import (
    DastAlertInfo, DastAlertInstanceSummarizedList, DastAlertLevelResultList,
    DastGroups, DastVulnerabilitySummary, DastTimeSpanRiskSummary,
    DastTopFiveRisks, DastResultsStatesSummary, DastComplianceAnalytics,
    DastComplianceOverTimeResponse, DastAlertLevelOccurrencesResponse,
    DastRiskLevelOverTimeResponse, DastStatesOverTimeResponse,
    DastManualFindingInstanceResultList, DastManualFindingsAlertLevelResultList,
    DastScreenshot, DastPentestFindingResult,
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
def scan_id(env_with_scan):
    scans = get_scans(environment_id=env_with_scan.environment_id, to=10)
    scan = next((s for s in scans.scans if s.has_results), None)
    if scan is None:
        pytest.skip("No scan with results on this tenant")
    return scan.scan_id


@pytest.fixture(scope="session")
def alert_id(env_with_scan, scan_id):
    results = get_alert_level_results(
        env_with_scan.environment_id, scan_id, page=1, per_page=1
    )
    if not results.results:
        pytest.skip("Scan has no alert-level results")
    return results.results[0].alert_similarity_id


@pytest.fixture(scope="session")
def app_with_no_dast_environment():
    """An Application that has no DAST Environment -- used to exercise
    the 204-No-Content "no data" path on states_summary/compliance.
    Found by probing get_results_states_summary itself (there's no
    "has DAST environment" flag on the Application list), since a 204
    there is the one directly observable signal of "no DAST Environment".
    """
    apps = _ApplicationsAPI().get_a_list_of_applications(limit=50)
    for app in apps.applications:
        if get_results_states_summary(app.id) is None:
            return app.id
    pytest.skip("No Application without a DAST Environment on this tenant")


# ----- Health check -----


def test_health_check():
    result = health_check()
    assert isinstance(result, str)
    assert result


# ----- Alert-level results -----


def test_get_alert_level_results(env_with_scan, scan_id):
    results = get_alert_level_results(
        env_with_scan.environment_id, scan_id, page=1, per_page=5
    )
    assert isinstance(results, DastAlertLevelResultList)
    assert results.total is not None and results.total >= 0


def test_get_alert_info(env_with_scan, scan_id, alert_id):
    info = get_alert_info(env_with_scan.environment_id, scan_id, alert_id)
    assert isinstance(info, DastAlertInfo)
    assert info.name


def test_get_alert_instances(env_with_scan, scan_id, alert_id):
    instances = get_alert_instances(
        env_with_scan.environment_id, scan_id, alert_id, page=1, per_page=5
    )
    assert isinstance(instances, DastAlertInstanceSummarizedList)
    assert instances.total is not None and instances.total >= 1
    assert instances.instances


def test_get_grouped_alert_level_results(env_with_scan, scan_id):
    groups = get_grouped_alert_level_results(
        env_with_scan.environment_id, scan_id, group=["severity"]
    )
    assert isinstance(groups, list)
    assert all(isinstance(g, DastGroups) for g in groups)


def test_post_alert_level_results(env_with_scan, scan_id):
    results = post_alert_level_results(
        env_with_scan.environment_id, scan_id, body={"page": 1, "per_page": 5}
    )
    assert isinstance(results, DastAlertLevelResultList)


def test_post_grouped_alert_level_results(env_with_scan, scan_id):
    groups = post_grouped_alert_level_results(
        env_with_scan.environment_id, scan_id, body={"group": ["severity"]}
    )
    assert isinstance(groups, list)
    assert all(isinstance(g, DastGroups) for g in groups)


def test_get_full_scan_results(env_with_scan, scan_id):
    result = get_full_scan_results(env_with_scan.environment_id, scan_id)
    assert isinstance(result, dict)
    assert "alerts" in result


def test_get_latest_correlation_results(env_with_scan, scan_id, alert_id):
    try:
        get_latest_correlation_results(
            env_with_scan.environment_id, scan_id,
            similarity_id=alert_id, type="alert",
        )
    except ValueError as e:
        # 403s on tenants without the DAST-code correlation feature flag.
        _skip_on_client_error(e)


def test_is_alert_level_enabled():
    assert isinstance(is_alert_level_enabled(), (bool, type(None)))


# ----- Scan-level summaries -----


def test_get_vulnerability_summary(env_with_scan, scan_id):
    summary = get_vulnerability_summary(env_with_scan.environment_id, scan_id)
    assert isinstance(summary, DastVulnerabilitySummary)
    assert summary.total_vulnerabilities is not None


def test_get_aging_summary(scan_id):
    summary = get_aging_summary(scan_id)
    assert isinstance(summary, DastTimeSpanRiskSummary)


def test_get_top_five_risks(scan_id):
    risks = get_top_five_risks(scan_id)
    assert isinstance(risks, list)
    assert all(isinstance(r, DastTopFiveRisks) for r in risks)


def test_get_scan_sites_tree(env_with_scan, scan_id):
    tree = get_scan_sites_tree(env_with_scan.environment_id, scan_id)
    assert isinstance(tree, list)


def test_get_instance_findings(env_with_scan, scan_id, alert_id):
    instances = get_alert_instances(
        env_with_scan.environment_id, scan_id, alert_id, page=1, per_page=1
    )
    if not instances.instances:
        pytest.skip("Alert has no instances")
    sim_id_2 = instances.instances[0].similarity_id_2
    finding = get_instance_findings(scan_id, env_with_scan.environment_id, sim_id_2)
    assert isinstance(finding, dict)


# ----- Analytics & overview (time series) -----


def test_get_results_states_summary_no_data(app_with_no_dast_environment):
    result = get_results_states_summary(app_with_no_dast_environment)
    assert result is None or isinstance(result, DastResultsStatesSummary)


def test_get_compliance_analytics_no_data(app_with_no_dast_environment):
    result = get_compliance_analytics(app_with_no_dast_environment)
    assert result is None or isinstance(result, DastComplianceAnalytics)


def test_get_compliance_over_time(env_with_scan):
    result = get_compliance_over_time(
        env_with_scan.environment_id, "2020-01-01T00:00:00Z", "2030-01-01T00:00:00Z"
    )
    assert isinstance(result, DastComplianceOverTimeResponse)


def test_get_occurrences_over_time(env_with_scan):
    result = get_occurrences_over_time(
        env_with_scan.environment_id,
        start="2020-01-01T00:00:00Z", end="2030-01-01T00:00:00Z",
    )
    assert isinstance(result, DastAlertLevelOccurrencesResponse)


def test_get_risk_level_over_time(env_with_scan):
    result = get_risk_level_over_time(
        env_with_scan.environment_id, "2020-01-01T00:00:00Z", "2030-01-01T00:00:00Z"
    )
    assert isinstance(result, DastRiskLevelOverTimeResponse)


def test_get_states_over_time(env_with_scan):
    result = get_states_over_time(
        env_with_scan.environment_id, "2020-01-01T00:00:00Z", "2030-01-01T00:00:00Z"
    )
    assert isinstance(result, DastStatesOverTimeResponse)


# ----- Manual findings lifecycle -----


def test_manual_findings_lifecycle(env_with_scan, scan_id):
    env_id = env_with_scan.environment_id
    finding = {
        "name": "SDK Test Manual Finding",
        "severity": "LOW",
        "risks": [{
            "severity": "LOW", "method": "GET",
            "url": "https://sdk-test.invalid/path", "path": "/path",
        }],
    }
    batch_id = create_manual_findings_batch(env_id, scan_id, findings=[finding])
    assert batch_id

    alert_id_ = None
    instance_id = None
    try:
        collection = get_manual_findings(env_id, scan_id)
        assert isinstance(collection, DastManualFindingInstanceResultList)
        match = next(
            (r for r in collection.results if r.name == "SDK Test Manual Finding"),
            None,
        )
        assert match is not None
        alert_id_ = match.alert_id
        instance_id = match.risk_id

        info = get_manual_finding_alert_info(env_id, scan_id, alert_id_)
        assert isinstance(info, DastAlertInfo)

        detail = get_manual_finding_instance_info(env_id, scan_id, instance_id)
        assert detail.id == instance_id

        screenshots = get_manual_finding_instance_screenshots(
            env_id, scan_id, instance_id
        )
        assert isinstance(screenshots, list)

        alert_level = get_manual_findings_alert_level(env_id, scan_id, page=1, per_page=5)
        assert isinstance(alert_level, DastManualFindingsAlertLevelResultList)

        grouped_alert_level = get_grouped_manual_findings_alert_level(
            env_id, scan_id, group=["severity"]
        )
        assert isinstance(grouped_alert_level, list)

        grouped = get_grouped_manual_findings(env_id, scan_id, group=["severity"])
        assert isinstance(grouped, list)

        # `state` is required live despite being documented as optional
        # (mutually exclusive with custom_state_id only).
        assert update_manual_finding_alert(env_id, scan_id, update={
            "result_id": alert_id_, "severity": "MEDIUM",
            "name": "SDK Test Manual Finding (updated)",
            "status": "New", "state": "Confirmed",
        }) is True

        assert update_manual_finding_instance(env_id, scan_id, update={
            "result_id": instance_id, "severity": "MEDIUM", "status": "New",
            "state": "Confirmed", "url": "https://sdk-test.invalid/path",
            "path": "/path", "method": "GET",
        }) is True

        assert update_manual_finding_alert_instance(env_id, scan_id, update={
            "instance_id": instance_id, "severity": "HIGH", "status": "New",
            "state": "Confirmed", "url": "https://sdk-test.invalid/path",
            "path": "/path", "method": "GET",
        }) is True

        assert unlink_manual_findings(env_id, scan_id, option="current_scan") is True
    finally:
        # Clean up regardless of how far the test got.
        try:
            if instance_id:
                delete_manual_finding_instances(
                    env_id, scan_id, alert_id=alert_id_, instance_ids=[instance_id]
                )
        except ValueError:
            pass
        try:
            if alert_id_:
                remaining = get_manual_findings(env_id, scan_id)
                if any(r.alert_id == alert_id_ for r in remaining.results):
                    delete_manual_finding_alerts(env_id, scan_id, alert_ids=[alert_id_])
        except ValueError:
            pass


# ----- Instance screenshots -----


def test_instance_screenshots_lifecycle(env_with_scan, scan_id, alert_id):
    env_id = env_with_scan.environment_id
    instances = get_alert_instances(env_id, scan_id, alert_id, page=1, per_page=1)
    if not instances.instances:
        pytest.skip("Alert has no instances")
    sim_id_2 = instances.instances[0].similarity_id_2

    # Minimal 1x1 PNG.
    import base64
    png = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk"
        "+A8AAQUBAScY42YAAAAASUVORK5CYII="
    )
    import tempfile
    import os as _os
    fd, path = tempfile.mkstemp(suffix=".png")
    try:
        with _os.fdopen(fd, "wb") as fh:
            fh.write(png)

        screenshot_ids = upload_instance_screenshots(env_id, sim_id_2, screenshots=[path])
        assert screenshot_ids
        try:
            screenshots = get_instance_screenshots(env_id, sim_id_2)
            assert any(isinstance(s, DastScreenshot) and s.id in screenshot_ids for s in screenshots)
        finally:
            assert delete_instance_screenshots(
                env_id, sim_id_2, screenshot_ids=screenshot_ids
            ) is True
    finally:
        _os.remove(path)


# ----- Pentest findings -----


def test_pentest_findings_endpoints(env_with_scan):
    env_id = env_with_scan.environment_id
    fake_pentest_scan_id = "00000000-0000-0000-0000-000000000000"

    findings = get_pentest_findings(env_id, fake_pentest_scan_id)
    assert isinstance(findings, list)
    assert all(isinstance(f, DastPentestFindingResult) for f in findings)

    details = get_pentest_finding_details(
        env_id, fake_pentest_scan_id, "00000000-0000-0000-0000-000000000000"
    )
    assert isinstance(details, dict)

    coverage = get_pentest_wstg_coverage(env_id, fake_pentest_scan_id)
    assert isinstance(coverage, dict)
    assert "categories" in coverage
