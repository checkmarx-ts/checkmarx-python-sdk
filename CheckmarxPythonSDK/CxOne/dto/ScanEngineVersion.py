from dataclasses import dataclass


@dataclass
class ScanEngineVersion:
    """

    Attributes:
        scan_id (str):
        project_id (str):
        tenant_id (str):
        engine_version (str):
    """
    scan_id: str
    project_id: str
    tenant_id: str
    engine_version: str


def construct_scan_engine_version(item):
    return ScanEngineVersion(
        scan_id=item.get("scanId"),
        project_id=item.get("projectId"),
        tenant_id=item.get("tenantId"),
        engine_version=item.get("engineVersion")
    )
