from dataclasses import dataclass
from typing import Optional


@dataclass
class LDAPGroupAndRoleMappingDetail:
    role_id: Optional[int] = None
    ldap_group_dn: Optional[str] = None
    ldap_group_display_name: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "roleId": self.role_id,
            "ldapGroupDn": self.ldap_group_dn,
            "ldapGroupDisplayName": self.ldap_group_display_name,
        }
