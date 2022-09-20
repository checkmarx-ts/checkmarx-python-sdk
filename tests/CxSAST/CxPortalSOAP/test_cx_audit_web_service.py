from CheckmarxPythonSDK.CxPortalSoapApiSDK import (
    get_files_extensions,
    get_source_code_for_scan,
)


def test_get_files_extensions():
    response = get_files_extensions()
    assert response is not None


def test_get_source_code_for_scan():

    scan_id = 1010032
    response = get_source_code_for_scan(scan_id=scan_id)
    assert response is not None
