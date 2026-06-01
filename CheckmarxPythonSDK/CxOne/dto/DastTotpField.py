from dataclasses import dataclass


@dataclass
class DastTotpField:
    """authSettings.totpField entry on POST /api/dast/scans/environment."""
    attribute: str = None
    value: str = None

    def to_dict(self) -> dict:
        raw = {"attribute": self.attribute, "value": self.value}
        return {k: v for k, v in raw.items() if v is not None}
