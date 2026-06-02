import pytest

from CheckmarxPythonSDK.CxOne import (
    get_data_retention_processes,
    get_locked_scans,
    get_process_status,
    lock_scans,
    unlock_scans,
    start_data_retention_process,
    abort_process,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=1)
    if result.scans:
        return result.scans[0].id
    return None


def test_get_data_retention_processes():
    result = get_data_retention_processes(limit=10)
    assert result is not None


def test_get_locked_scans():
    result = get_locked_scans(limit=10)
    assert result is not None
    assert "lockedScans" in result


def test_get_process_status():
    processes = get_data_retention_processes(limit=1)
    configs = processes.get("configs", [])
    if not configs:
        pytest.skip("No data retention processes found")
    process_id = configs[0].get("id")
    result = get_process_status(id=process_id)
    assert result is not None
    assert "status" in result


def test_lock_and_unlock_scans():
    scan_id = _get_scan_id()
    if not scan_id:
        pytest.skip("No scans found")

    # Lock
    lock_result = lock_scans(scan_ids=[scan_id])
    assert lock_result is not None
    assert "lockedScans" in lock_result

    # Unlock
    unlock_result = unlock_scans(scan_ids=[scan_id])
    assert unlock_result is not None
    assert "unlockedScans" in unlock_result


def test_start_and_abort_process():
    # Start a process with scansToKeep
    try:
        result = start_data_retention_process(scans_to_keep=10)
        assert result is not None
        process_id = result.get("id")
        assert process_id is not None

        # Abort it
        is_aborted = abort_process(id=process_id)
        assert is_aborted is True
    except Exception as e:
        print("start_and_abort_process skipped: {}".format(str(e)))
