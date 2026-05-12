# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxOsaLicense:
    """
    the license of a third party library
    """

    id: Optional[str] = None
    name: Optional[str] = None
    risk_level: Optional[str] = None
    copyright_risk_score: Optional[int] = None
    patent_risk_score: Optional[int] = None
    copy_left: Optional[str] = None
    linking: Optional[str] = None
    royalty_free: Optional[str] = None
    reference_type: Optional[str] = None
    reference: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxOsaLicense":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            risk_level=item.get("riskLevel"),
            copyright_risk_score=item.get("copyrightRiskScore"),
            patent_risk_score=item.get("patentRiskScore"),
            copy_left=item.get("copyLeft"),
            linking=item.get("linking"),
            royalty_free=item.get("royalityFree"),  # Note: API typo
            reference_type=item.get("referenceType"),
            reference=item.get("reference"),
            url=item.get("url"),
        )
