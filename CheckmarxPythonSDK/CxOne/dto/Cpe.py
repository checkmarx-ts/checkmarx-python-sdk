from dataclasses import dataclass
from typing import Optional


@dataclass
class Cpe:
    """An entry in VulnerabilityDetail.cpes."""
    vendor: Optional[str] = None
    product: Optional[str] = None
    version: Optional[str] = None
    version_label: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Cpe":
        return cls(
            vendor=item.get("vendor"),
            product=item.get("product"),
            version=item.get("version"),
            version_label=item.get("versionLabel"),
        )
