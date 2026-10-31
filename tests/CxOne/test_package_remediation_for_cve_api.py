import pytest

from CheckmarxPythonSDK.CxOne import get_package_remediation_for_cve
from CheckmarxPythonSDK.CxOne.dto import PackageVersionRemediation


def test_get_package_remediation_for_cve():
    result = get_package_remediation_for_cve(
        package_type="npm",
        name="lodash",
        package_version="4.17.21",
        cve="CVE-2025-13465",
    )
    assert isinstance(result, PackageVersionRemediation)
    assert result.current is not None
    assert result.current.version == "4.17.21"
    assert result.nearest is not None
    assert result.latest is not None


def test_get_package_remediation_for_cve_with_scoped_package_name():
    # scoped npm package name contains "/", which must be URL-encoded
    result = get_package_remediation_for_cve(
        package_type="npm",
        name="@babel/core",
        package_version="7.0.0",
        cve="CVE-2025-13465",
    )
    assert isinstance(result, PackageVersionRemediation)
    assert result.current.version == "7.0.0"


def test_get_package_remediation_for_cve_not_found():
    with pytest.raises(ValueError):
        get_package_remediation_for_cve(
            package_type="npm",
            name="lodash",
            package_version="4.17.21",
            cve="CVE-0000-0000",
        )
