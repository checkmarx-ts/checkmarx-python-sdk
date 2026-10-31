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
    assert isinstance(risk.suspected_malware, list)

    # package.remediation -> PackageVersionRemediation/RemediationVersionCounts
    remediation = risk.package.remediation
    assert remediation is not None
    for counts in (remediation.latest, remediation.nearest, remediation.current):
        assert counts is not None
        assert counts.version is not None
        assert counts.critical_vulnerabilities is not None
        assert counts.high_vulnerabilities is not None
        assert counts.medium_vulnerabilities is not None
        assert counts.low_vulnerabilities is not None
        assert counts.none_vulnerabilities is not None
    assert remediation.current.version == "4.17.21"

    # vulnerabilities[].details -> VulnerabilityDetail and its nested DTOs
    # (Cvss3/Epss/references/cpes observed present on every lodash CVE;
    # Cvss4 only on some, so checked conditionally rather than assumed)
    assert len(risk.vulnerabilities) > 0
    found_cvss3 = found_cvss4 = found_epss = False
    found_reference = found_vulnerable_path = found_cpe = False
    for vuln in risk.vulnerabilities:
        assert vuln.id is not None
        assert vuln.cve is not None
        assert vuln.cx_id is not None
        assert vuln.severity is not None
        assert vuln.details is not None
        assert vuln.details.cwe is not None
        assert vuln.details.description is not None

        if vuln.details.cvss3 is not None:
            found_cvss3 = True
            assert vuln.details.cvss3.base_score is not None
            assert vuln.details.cvss3.severity is not None
            assert vuln.details.cvss3.vector is not None
        if vuln.details.cvss4 is not None:
            found_cvss4 = True
            assert vuln.details.cvss4.base_score is not None
            assert vuln.details.cvss4.vector is not None
        if vuln.details.epss is not None:
            found_epss = True
            assert vuln.details.epss.epss is not None
            assert vuln.details.epss.percentile is not None
        if vuln.details.references:
            found_reference = True
            assert vuln.details.references[0].url is not None
        if vuln.details.vulnerable_paths:
            found_vulnerable_path = True
            assert vuln.details.vulnerable_paths[0].file_name is not None
        if vuln.details.cpes:
            found_cpe = True
            assert vuln.details.cpes[0].product is not None

    # cvss3/epss/references/cpes observed on every lodash CVE at write
    # time; cvss4 only on some, so not asserted unconditionally.
    assert found_cvss3
    assert found_epss
    assert found_reference
    assert found_cpe
    if not found_cvss4:
        import logging
        logging.getLogger(__name__).warning(
            "No vulnerability in this response carried cvss4 -- "
            "Cvss4 DTO parsing not exercised by this test run."
        )


def test_get_package_risks_sparse_risk_score_fields():
    # package_reliability/runtime_behavior/contributor_reputation are
    # undocumented and sparse -- known-flagged ua-parser-js@0.7.29 (the
    # same test-malicious-version used elsewhere in this SDK, see
    # CxScaApiSDK/api.py) reliably has them populated, unlike lodash.
    items = [PackageRiskItem(type="npm", name="ua-parser-js", version="0.7.29")]
    result = get_package_risks(
        items=items,
        include_risk_details=True,
        include_version_details=True,
        include_version_remediation=True,
    )
    assert len(result) == 1
    package = result[0].package
    assert package.status == "Ok"
    assert package.package_reliability is not None
    assert package.runtime_behavior is not None
    assert package.contributor_reputation is not None


def test_get_package_risks_not_found():
    items = [PackageRiskItem(type="npm", name="this-package-does-not-exist-xyz", version="0.0.0")]
    result = get_package_risks(items=items)
    assert len(result) == 1
    risk = result[0]
    assert risk.package.status == "NotFound"
    assert risk.vulnerabilities == []
    assert risk.suspected_malware == []
