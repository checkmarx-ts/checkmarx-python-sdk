from dataclasses import dataclass


@dataclass
class DastScanInsight:
    """One entry in DastScan.insights — surfaces scanner warnings/info
    like "ZAP errors logged" etc. Undocumented field surfaced via the
    live API."""
    level: str = None
    reason: str = None
    site: str = None
    key: str = None
    description: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScanInsight":
        return cls(
            level=item.get("level"),
            reason=item.get("reason"),
            site=item.get("site"),
            key=item.get("key"),
            description=item.get("description"),
        )
