from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Cvss3:
    """VulnerabilityDetail.cvss3 -- CVSS v3.x score breakdown."""
    base_score: Optional[Union[float, str]] = None
    severity: Optional[str] = None
    attack_vector: Optional[str] = None
    attack_complexity: Optional[str] = None
    privileges_required: Optional[str] = None
    user_interaction: Optional[str] = None
    scope: Optional[str] = None
    integrity_impact: Optional[str] = None
    availability_impact: Optional[str] = None
    confidentiality_impact: Optional[str] = None
    vector: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Cvss3":
        return cls(
            base_score=item.get("baseScore"),
            severity=item.get("severity"),
            attack_vector=item.get("attackVector"),
            attack_complexity=item.get("attackComplexity"),
            privileges_required=item.get("privilegesRequired"),
            user_interaction=item.get("userInteraction"),
            scope=item.get("scope"),
            integrity_impact=item.get("integrityImpact"),
            availability_impact=item.get("availabilityImpact"),
            confidentiality_impact=item.get("confidentialityImpact"),
            vector=item.get("vector"),
        )
