from dataclasses import dataclass
from typing import Optional


@dataclass
class LDAPTeamMapping:
    id: Optional[int] = None
    ldap_server_id: Optional[int] = None
    team_id: Optional[int] = None
    ldap_group_dn: Optional[str] = None
    ldap_group_display_name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "LDAPTeamMapping":
        return cls(
            id=item.get("id"),
            ldap_server_id=item.get("ldapServerId"),
            team_id=item.get("teamId"),
            ldap_group_dn=item.get("ldapGroupDn"),
            ldap_group_display_name=item.get("ldapGroupDisplayName"),
        )
