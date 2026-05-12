from dataclasses import dataclass


@dataclass
class ScopePermissions:
    view: ... = None
    manage: ... = None
    view_members: ... = None
    manage_members: ... = None
    manage_membership: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScopePermissions":
        return cls(
            view=item.get("view"),
            manage=item.get("manage"),
            view_members=item.get("view-members"),
            manage_members=item.get("manage-members"),
            manage_membership=item.get("manage-membership"),
        )
