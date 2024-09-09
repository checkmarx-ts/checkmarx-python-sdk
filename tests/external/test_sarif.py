from CheckmarxPythonSDK.external.sarif import (
    create_sarif_report_from_sast_xml
)

from CheckmarxPythonSDK.external.sarif.dto import (
    SarifResultsCollection
)

from CheckmarxPythonSDK.CxRestAPISDK.CxSastXML.xml_results import obj_to_dict


def test_sast_xml_to_sarif():
    sarif_result: SarifResultsCollection = create_sarif_report_from_sast_xml(r"D:\Downloads\Java-Vulnerable-Lab.xml")
    sarif_result_dict: dict = obj_to_dict(sarif_result)
    import json
    with open("jvl.sarif", "w") as json_file:
        json.dump(sarif_result_dict, json_file)
    assert sarif_result_dict is not None
