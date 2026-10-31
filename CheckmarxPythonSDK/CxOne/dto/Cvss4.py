from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Cvss4:
    """VulnerabilityDetail.cvss4 -- CVSS v4.0 score breakdown. Not every
    vulnerability has one (observed absent on the live tenant even when
    cvss3 is present).
    """
    base_score: Optional[Union[float, str]] = None
    attack_vector: Optional[str] = None
    attack_complexity: Optional[str] = None
    attack_requirements: Optional[str] = None
    privileges_required: Optional[str] = None
    user_interaction: Optional[str] = None
    vulnerable_system_confidentiality: Optional[str] = None
    vulnerable_system_integrity: Optional[str] = None
    vulnerable_system_availability: Optional[str] = None
    subsequent_system_confidentiality: Optional[str] = None
    subsequent_system_integrity: Optional[str] = None
    subsequent_system_availability: Optional[str] = None
    exploit_maturity: Optional[str] = None
    confidentiality_requirement: Optional[str] = None
    integrity_requirement: Optional[str] = None
    availability_requirement: Optional[str] = None
    severity: Optional[str] = None
    vector: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Cvss4":
        return cls(
            base_score=item.get("baseScore"),
            attack_vector=item.get("attackVector"),
            attack_complexity=item.get("attackComplexity"),
            attack_requirements=item.get("attackRequirements"),
            privileges_required=item.get("privilegesRequired"),
            user_interaction=item.get("userInteraction"),
            vulnerable_system_confidentiality=item.get("vulnerableSystemConfidentiality"),
            vulnerable_system_integrity=item.get("vulnerableSystemIntegrity"),
            vulnerable_system_availability=item.get("vulnerableSystemAvailability"),
            subsequent_system_confidentiality=item.get("subsequentSystemConfidentiality"),
            subsequent_system_integrity=item.get("subsequentSystemIntegrity"),
            subsequent_system_availability=item.get("subsequentSystemAvailability"),
            exploit_maturity=item.get("exploitMaturity"),
            confidentiality_requirement=item.get("confidentialityRequirement"),
            integrity_requirement=item.get("integrityRequirement"),
            availability_requirement=item.get("availabilityRequirement"),
            severity=item.get("severity"),
            vector=item.get("vector"),
        )
