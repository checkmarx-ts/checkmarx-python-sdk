from dataclasses import dataclass, field
from typing import List

from .PackageRiskItem import PackageRiskItem


@dataclass
class PackageRisksRequest:
    """Request body for POST /api/v1/Packages/risks (SCA Data Hub
    service). Maximum 100 items per request (server-enforced).
    """
    format: str = "Package"  # "Package" or "Purl"
    items: List[PackageRiskItem] = field(default_factory=list)
