class ScopePermissions:

    def __init__(self, view, manage, view_members, manage_members, manage_membership):
        self.view = view
        self.manage = manage
        self.view_members = view_members
        self.manage_members = manage_members
        self.manage_membership = manage_membership

    def __str__(self):
        return f"ScopePermissions(" \
               f"view={self.view} " \
               f"manage={self.manage} " \
               f"view_members={self.view_members} " \
               f"manage_members={self.manage_members} " \
               f"manage_membership={self.manage_membership} " \
               f")"

    def to_dict(self):
        return {
                'view': self.view,
                'manage': self.manage,
                'view-members': self.view_members,
                'manage-members': self.manage_members,
                'manage-membership': self.manage_membership
            }


def construct_scope_permissions(item):
    return ScopePermissions(
        view=item.get("view"),
        manage=item.get("manage"),
        view_members=item.get("view-members"),
        manage_members=item.get("manage-members"),
        manage_membership=item.get("manage-membership")
    )
