from CheckmarxPythonSDK.CxOne.scaAPI import ScaAPI


def test_get_projects():
    projects = ScaAPI().get_all_projects()
    assert projects is not None


def test_get_count_of_vulnerabilities_risks_by_scan_id():
    result = ScaAPI().get_count_of_vulnerabilities_risks_by_scan_id(scan_id="d201a795-e2f0-44bf-8f5a-d6a5eb1c28b7")
    assert result is not None
