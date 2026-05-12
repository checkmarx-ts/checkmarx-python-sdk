from dataclasses import dataclass
from .ScopePermissions import ScopePermissions


@dataclass
class ManagementPermissionReference:
    enabled: ... = None
    resource: ... = None
    scope_permissions: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ManagementPermissionReference":
        return cls(
            enabled=item.get("enabled"),
            resource=item.get("resource"),
            scope_permissions=ScopePermissions.from_dict(item.get("scopePermissions")),
        )
