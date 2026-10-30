from dataclasses import dataclass
from typing import Optional


@dataclass
class DastCorrelationScanSettings:
    """The `settings` field on CorrelationScanResponse."""
    mode: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastCorrelationScanSettings":
        return cls(mode=item.get("mode"))
