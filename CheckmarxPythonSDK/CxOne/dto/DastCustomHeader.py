from dataclasses import dataclass


@dataclass
class DastCustomHeader:
    """settings.customHeaders[] entry on POST /api/dast/scans/environment.

    header and value are required by the API.
    """
    header: str = None
    value: str = None
    url: str = None

    def to_dict(self) -> dict:
        raw = {"header": self.header, "value": self.value, "url": self.url}
        return {k: v for k, v in raw.items() if v is not None}
