from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI
from CheckmarxPythonSDK.CxPortalSoapApiSDK import (
    get_files_extensions,
    get_source_code_for_scan,
)
from .. import get_project_id


def _get_scan_id():
    project_id = get_project_id()
    scan_api = ScansAPI()
    return scan_api.get_last_scan_id_of_a_project(
        project_id,
        only_finished_scans=True,
        only_completed_scans=True,
        only_real_scans=True,
        only_full_scans=True,
    )


def test_get_files_extensions():
    response = get_files_extensions()
    assert response is not None


def test_get_source_code_for_scan():
    scan_id = _get_scan_id()
    response = get_source_code_for_scan(scan_id=scan_id)
    assert response is not None
