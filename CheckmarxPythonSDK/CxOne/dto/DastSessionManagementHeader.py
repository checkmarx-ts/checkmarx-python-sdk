from dataclasses import dataclass


@dataclass
class DastSessionManagementHeader:
    """settings.sessionManagement[] entry on POST /api/dast/scans/environment.

    Distinct from the response-side DastSessionManagement, which has
    method/parameters fields. Here each entry is a simple header/value
    pair used for session tracking.
    """
    header: str = None
    value: str = None

    def to_dict(self) -> dict:
        raw = {"header": self.header, "value": self.value}
        return {k: v for k, v in raw.items() if v is not None}
