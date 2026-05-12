from dataclasses import dataclass
from typing import Optional


@dataclass
class SAMLRoleMapping:
    id: Optional[int] = None
    saml_identity_provider_id: Optional[int] = None
    role_id: Optional[int] = None
    role_name: Optional[str] = None
    saml_attribute_value: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "SAMLRoleMapping":
        return cls(
            id=item.get("id"),
            saml_identity_provider_id=item.get("samlIdentityProviderId"),
            role_id=item.get("roleId"),
            role_name=item.get("roleName"),
            saml_attribute_value=item.get("samlAttributeValue"),
        )
