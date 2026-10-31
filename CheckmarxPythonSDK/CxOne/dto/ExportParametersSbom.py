from dataclasses import dataclass


@dataclass
class ExportParametersSbom:
    """exportParameters for POST /api/sca/export/requests when
    fileFormat is CycloneDxJson, CycloneDxXml, or SpdxJson.
    """
    hideDevAndTestDependencies: bool = False
    showOnlyEffectiveLicenses: bool = False
