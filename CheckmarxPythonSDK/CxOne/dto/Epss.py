from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Epss:
    """VulnerabilityDetail.epss -- Exploit Prediction Scoring System."""
    epss: Optional[Union[float, str]] = None
    percentile: Optional[Union[float, str]] = None
    date: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Epss":
        return cls(
            epss=item.get("epss"),
            percentile=item.get("percentile"),
            date=item.get("date"),
        )
