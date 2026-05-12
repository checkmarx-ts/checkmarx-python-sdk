from dataclasses import dataclass
from typing import Optional


@dataclass
class LDAPRoleMapping:
    id: Optional[int] = None
    ldap_server_id: Optional[int] = None
    role_id: Optional[int] = None
    ldap_group_dn: Optional[str] = None
    ldap_group_display_name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "LDAPRoleMapping":
        return cls(
            id=item.get("id"),
            ldap_server_id=item.get("ldapServerId"),
            role_id=item.get("roleId"),
            ldap_group_dn=item.get("ldapGroupDn"),
            ldap_group_display_name=item.get("ldapGroupDisplayName"),
        )
