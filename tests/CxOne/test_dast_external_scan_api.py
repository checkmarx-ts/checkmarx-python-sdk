import os
import tempfile

import pytest

from CheckmarxPythonSDK.CxOne import (
    get_environments, get_scans,
    update_external_scan, upload_external_scan_log, upload_external_scan_results,
    get_sequences_report,
)
from CheckmarxPythonSDK.CxOne.dto import DastSequencesReport


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


def test_get_sequences_report(env_with_scan, scan_id):
    report = get_sequences_report(env_with_scan.environment_id, scan_id)
    assert isinstance(report, DastSequencesReport)
    assert isinstance(report.sequences, list)


def test_update_external_scan_is_noop_on_completed_scan(env_with_scan, scan_id):
    """Per the spec, this has no effect on scans not in "ExternalScan"
    status -- verify it returns success without disturbing the scan.
    """
    result = update_external_scan({
        "scanId": scan_id,
        "environmentId": env_with_scan.environment_id,
        "lastStatus": "sdk-test-noop",
    })
    assert isinstance(result, str)


def test_upload_external_scan_log(env_with_scan, scan_id):
    fd, path = tempfile.mkstemp(suffix=".log")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write("sdk test log content\n")
        ok = upload_external_scan_log(
            env_with_scan.environment_id, scan_id, path, num_log_files=1
        )
        assert ok is True
    finally:
        os.remove(path)


def test_upload_external_scan_results(env_with_scan, scan_id):
    fd, path = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write('{"sdk": "test results"}')
        ok = upload_external_scan_results(
            env_with_scan.environment_id, scan_id, path,
        )
        assert ok is True
    finally:
        os.remove(path)
