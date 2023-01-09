from CheckmarxPythonSDK.external.sarif import (
    create_sarif_report_from_sast_xml
)

from CheckmarxPythonSDK.external.sarif.dto import (
    SarifResultsCollection
)

from CheckmarxPythonSDK.CxRestAPISDK.CxSastXML.xml_results import obj_to_dict


def test_sast_xml_to_sarif():
    sarif_result: SarifResultsCollection = create_sarif_report_from_sast_xml(r"C:\Users\HappyY\Documents\SourceCode\GitHub\checkmarx-python-sdk\examples\jvl_local_2022_10_18_16_39_47.XML")
    sarif_result_dict: dict = obj_to_dict(sarif_result)
    assert sarif_result_dict is not None
