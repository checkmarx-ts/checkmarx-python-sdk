from dataclasses import dataclass


@dataclass
class ExportParametersScanReport:
    """exportParameters for POST /api/sca/export/requests when
    fileFormat is ScanReportJson, ScanReportXml, ScanReportCsv, or
    ScanReportPdf.
    """
    hideDevAndTestDependencies: bool = False
    showOnlyEffectiveLicenses: bool = False
    excludePackages: bool = False
    excludeLicenses: bool = True
    excludeVulnerabilities: bool = False
    excludePolicies: bool = True
