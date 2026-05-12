from dataclasses import dataclass
from typing import Optional


@dataclass
class SAMLTeamMapping:
    id: Optional[int] = None
    saml_identity_provider_id: Optional[int] = None
    team_id: Optional[int] = None
    team_full_path: Optional[str] = None
    saml_attribute_value: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "SAMLTeamMapping":
        return cls(
            id=item.get("id"),
            saml_identity_provider_id=item.get("samlIdentityProviderId"),
            team_id=item.get("teamId"),
            team_full_path=item.get("teamFullPath"),
            saml_attribute_value=item.get("samlAttributeValue"),
        )
