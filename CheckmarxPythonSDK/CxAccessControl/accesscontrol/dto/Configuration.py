from dataclasses import dataclass
from typing import Optional


@dataclass
class Configuration:
    registration_link: Optional[str] = None
    is_assign_all_roles_by_manage_users_enabled: Optional[bool] = None
    is_multitenancy_mode: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Configuration":
        return cls(
            registration_link=item.get("registrationLink"),
            is_assign_all_roles_by_manage_users_enabled=item.get("isAssignAllRolesByManageUsersEnabled"),
            is_multitenancy_mode=item.get("isMultitenancyMode"),
        )
