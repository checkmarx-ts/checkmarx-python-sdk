import pathlib

from CheckmarxPythonSDK.CxRestAPISDK.sast.scans.dto.CxScanReportXmlContent import CxScanReportXmlContent

current_folder = pathlib.Path(__file__).parent.absolute()
xml_path = current_folder / "jvl_local.xml"


def test_filter_by_severity():
    xml_report = CxScanReportXmlContent(xml_path)
    xml_report.filter_by_severity(high=True)
    xml_report.write_new_xml("filter_by_severity.xml")


def test_filter_by_state():
    xml_report = CxScanReportXmlContent(xml_path)
    xml_report.filter_by_state(confirmed=True)
    xml_report.write_new_xml("filter_by_state.xml")


def test_filter_by_assign_to_user():
    xml_report = CxScanReportXmlContent(xml_path)
    xml_report.filter_by_assign_to_user(user_list=['Admin'])
    xml_report.write_new_xml("filter_by_assign_to_user.xml")


def test_filter_by_categories():
    xml_report = CxScanReportXmlContent(xml_path)
    xml_report.filter_by_categories(categories_list=["OWASP Top 10 2013"])
    xml_report.write_new_xml("filter_by_categories.xml")


def test_filter_by_query_names():
    xml_report = CxScanReportXmlContent(xml_path)
    xml_report.filter_by_query_names(query_names=["Stored_XSS"])
    xml_report.write_new_xml("filter_by_query_names.xml")
