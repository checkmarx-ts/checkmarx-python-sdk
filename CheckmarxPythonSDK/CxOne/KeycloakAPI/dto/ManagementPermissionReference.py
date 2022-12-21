from .ScopePermissions import ScopePermissions, construct_scope_permissions


class ManagementPermissionReference:
    def __init__(self, enabled: bool, resource: str, scope_permissions: ScopePermissions):
        """

        Args:
            enabled (bool):
            resource (str):
            scope_permissions ():
        """
        self.enabled = enabled
        self.resource = resource
        self.scopePermissions = scope_permissions

    def __str__(self):
        return f"ManagementPermissionReference(" \
               f"enabled={self.enabled} " \
               f"resource={self.resource} " \
               f"scopePermissions={self.scopePermissions} " \
               f")"

    def get_post_data(self):
        import json
        return json.dumps({
            "enabled": self.enabled,
            "resource": self.resource,
            "scopePermissions": self.scopePermissions.get_post_data(),
        })


def construct_management_permission_reference(item):
    return ManagementPermissionReference(
        enabled=item.get("enabled"),
        resource=item.get("resource"),
        scope_permissions=construct_scope_permissions(item.get("scopePermissions")),
    )
