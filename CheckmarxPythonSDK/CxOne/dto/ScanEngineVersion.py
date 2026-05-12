from dataclasses import dataclass


@dataclass
class ScanEngineVersion:
    scan_id: str = None
    project_id: str = None
    tenant_id: str = None
    engine_version: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScanEngineVersion":
        return cls(
            scan_id=item.get("scanId"),
            project_id=item.get("projectId"),
            tenant_id=item.get("tenantId"),
            engine_version=item.get("engineVersion"),
        )
