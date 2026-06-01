from dataclasses import dataclass


@dataclass
class RiskLevel:
    critical_count: int = None
    high_count: int = None
    medium_count: int = None
    low_count: int = None
    info_count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "RiskLevel":
        return cls(
            critical_count=item.get("criticalCount"),
            high_count=item.get("highCount"),
            medium_count=item.get("mediumCount"),
            low_count=item.get("lowCount"),
            info_count=item.get("infoCount"),
        )
