from dataclasses import dataclass


@dataclass
class DastAlertRiskLevel:
    # The doc spells the critical key "CriticalCount" (uppercase C) while
    # riskLevel uses "criticalCount". Accept both casings just in case.
    critical_count: int = None
    high_count: int = None
    medium_count: int = None
    low_count: int = None
    info_count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAlertRiskLevel":
        return cls(
            critical_count=item.get("CriticalCount", item.get("criticalCount")),
            high_count=item.get("highCount"),
            medium_count=item.get("mediumCount"),
            low_count=item.get("lowCount"),
            info_count=item.get("infoCount"),
        )
