from CheckmarxPythonSDK.CxRestAPISDK.CxSastXML import get_xml_results, get_xml_results_as_dict


def test_get_xml_results():
    result = get_xml_results(r"C:\Users\HappyY\Documents\SourceCode\GitHub\checkmarx-python-sdk\examples\jvl_local_2022_10_18_16_39_47.XML")
    assert result is not None


def test_get_xml_results_as_dict():
    result = get_xml_results_as_dict(r"C:\Users\HappyY\Documents\SourceCode\GitHub\checkmarx-python-sdk\examples\jvl_local_2022_10_18_16_39_47.XML")
    assert result is not None
