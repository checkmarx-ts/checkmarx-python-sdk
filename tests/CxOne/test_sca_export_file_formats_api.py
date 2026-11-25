from CheckmarxPythonSDK.CxOne import get_sca_export_file_formats
from CheckmarxPythonSDK.CxOne.dto import ScaExportFileFormats
from CheckmarxPythonSDK.CxOne.reportAPI import SCA_EXPORT_FILE_FORMATS


def test_get_sca_export_file_formats():
    result = get_sca_export_file_formats()
    assert isinstance(result, list)
    assert len(result) > 0
    for entry in result:
        assert isinstance(entry, ScaExportFileFormats)
        assert entry.route is not None
        assert isinstance(entry.file_formats, list)


def test_requests_route_file_formats_are_all_accepted_by_create_sca_scan_report():
    # cross-check: every fileFormat the live /requests route reports
    # (the route used by create_sca_scan_report) must be in the
    # accepted-formats set create_sca_scan_report validates against --
    # catches drift if Checkmarx adds/renames a format.
    result = get_sca_export_file_formats()
    requests_route = next(r for r in result if r.route == "/requests")
    assert set(requests_route.file_formats) <= SCA_EXPORT_FILE_FORMATS
