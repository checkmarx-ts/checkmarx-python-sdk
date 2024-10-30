from CheckmarxPythonSDK.CxOne import (
    get_all_feature_flags,
    get_feature_flag
)

def test_get_all_feature_flags_no_args():

    flags = get_all_feature_flags()
    assert flags is not None
    assert type(flags) is list


def test_get_all_feature_flags_one_flag():

    # This flag should be enabled in all tenants
    flags = get_all_feature_flags(["SBOM_SCAN_ENABLED"])
    assert flags is not None
    assert type(flags) is list
    assert len(flags) == 1
    assert flags[0].name == "SBOM_SCAN_ENABLED"
    assert flags[0].status


def test_get_all_feature_flags_two_flags():

    # These flags should be enabled in all tenants
    flags = get_all_feature_flags(["NEW_PROJECT_REPORT_ENABLED", "SBOM_SCAN_ENABLED"])
    assert flags is not None
    assert type(flags) is list
    assert len(flags) == 2
    flags = sorted(flags)
    assert flags[0].name == "NEW_PROJECT_REPORT_ENABLED"
    assert flags[0].status
    assert flags[1].name == "SBOM_SCAN_ENABLED"
    assert flags[1].status


def test_get_feature_flag():

    # This flag should be enabled in all tenants
    flag = get_feature_flag("SBOM_SCAN_ENABLED")
    assert flag is not None
    assert flag.name == "SBOM_SCAN_ENABLED"
    assert flag.status
