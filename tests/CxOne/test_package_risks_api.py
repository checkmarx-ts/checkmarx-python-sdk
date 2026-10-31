from CheckmarxPythonSDK.CxOne import get_package_risks
from CheckmarxPythonSDK.CxOne.dto import PackageRisk, PackageRiskItem


def test_get_package_risks_by_package():
    items = [PackageRiskItem(type="npm", name="lodash", version="4.17.21")]
    result = get_package_risks(items=items, format_="Package")
    assert isinstance(result, list)
    assert len(result) == 1
    risk = result[0]
    assert isinstance(risk, PackageRisk)
    assert risk.package.status == "Ok"
    assert risk.package.name == "lodash"
    assert isinstance(risk.vulnerabilities, list)


def test_get_package_risks_by_purl_with_details():
    items = [PackageRiskItem(purl="pkg:npm/lodash@4.17.21")]
    result = get_package_risks(
        items=items,
        format_="Purl",
        include_risk_details=True,
        include_version_details=True,
        include_version_remediation=True,
    )
    assert len(result) == 1
    risk = result[0]
    assert risk.package.status == "Ok"
    assert risk.package.purl == "pkg:npm/lodash@4.17.21"
    assert risk.package.remediation is not None
    assert risk.package.remediation.current is not None
    assert len(risk.vulnerabilities) > 0
    vuln = risk.vulnerabilities[0]
    assert vuln.cve is not None
    assert vuln.details is not None
    assert vuln.details.cwe is not None


def test_get_package_risks_not_found():
    items = [PackageRiskItem(type="npm", name="this-package-does-not-exist-xyz", version="0.0.0")]
    result = get_package_risks(items=items)
    assert len(result) == 1
    risk = result[0]
    assert risk.package.status == "NotFound"
    assert risk.vulnerabilities == []
    assert risk.suspected_malware == []
