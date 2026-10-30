from dataclasses import dataclass
from typing import Optional


@dataclass
class DastCorrelationCapacityResponse:
    """Response from GET /credits/correlation-capacity."""
    remaining_instances: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastCorrelationCapacityResponse":
        return cls(remaining_instances=item.get("remaining_instances"))
