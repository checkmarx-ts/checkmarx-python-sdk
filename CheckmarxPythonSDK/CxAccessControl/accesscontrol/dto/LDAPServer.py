from dataclasses import dataclass
from typing import Optional


@dataclass
class LDAPServer:
    id: Optional[int] = None
    active: Optional[bool] = None
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    use_ssl: Optional[bool] = None
    verify_ssl_certificate: Optional[bool] = None
    ldap_directory_type: Optional[str] = None
    sso_enabled: Optional[bool] = None
    mapped_domain_id: Optional[int] = None
    based_dn: Optional[str] = None
    additional_user_dn: Optional[str] = None
    user_object_filter: Optional[str] = None
    user_object_class: Optional[str] = None
    username_attribute: Optional[str] = None
    first_name_attribute: Optional[str] = None
    last_name_attribute: Optional[str] = None
    email_attribute: Optional[str] = None
    synchronization_enabled: Optional[bool] = None
    default_team_id: Optional[int] = None
    default_role_id: Optional[int] = None
    update_team_and_role_upon_login_enabled: Optional[bool] = None
    periodical_synchronization_enabled: Optional[bool] = None
    advanced_team_and_role_mapping_enabled: Optional[bool] = None
    additional_group_dn: Optional[str] = None
    group_object_class: Optional[str] = None
    group_object_filter: Optional[str] = None
    group_name_attribute: Optional[str] = None
    group_members_attribute: Optional[str] = None
    user_membership_attribute: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "LDAPServer":
        return cls(
            id=item.get("id"),
            active=item.get("active"),
            name=item.get("name"),
            host=item.get("host"),
            port=item.get("port"),
            username=item.get("username"),
            use_ssl=item.get("useSsl"),
            verify_ssl_certificate=item.get("verifySslCertificate"),
            ldap_directory_type=item.get("ldapDirectoryType"),
            sso_enabled=item.get("ssoEnabled"),
            mapped_domain_id=item.get("mappedDomainId"),
            based_dn=item.get("baseDn"),
            additional_user_dn=item.get("additionalUserDn"),
            user_object_filter=item.get("userObjectFilter"),
            user_object_class=item.get("userObjectClass"),
            username_attribute=item.get("usernameAttribute"),
            first_name_attribute=item.get("firstNameAttribute"),
            last_name_attribute=item.get("lastNameAttribute"),
            email_attribute=item.get("emailAttribute"),
            synchronization_enabled=item.get("synchronizationEnabled"),
            default_team_id=item.get("defaultTeamId"),
            default_role_id=item.get("defaultRoleId"),
            update_team_and_role_upon_login_enabled=item.get("updateTeamAndRoleUponLoginEnabled"),
            periodical_synchronization_enabled=item.get("periodicalSynchronizationEnabled"),
            advanced_team_and_role_mapping_enabled=item.get("advancedTeamAndRoleMappingEnabled"),
            additional_group_dn=item.get("additionalGroupDn"),
            group_object_class=item.get("groupObjectClass"),
            group_object_filter=item.get("groupObjectFilter"),
            group_name_attribute=item.get("groupNameAttribute"),
            group_members_attribute=item.get("groupMembersAttribute"),
            user_membership_attribute=item.get("userMembershipAttribute"),
        )
