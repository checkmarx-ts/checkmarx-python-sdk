from dataclasses import dataclass
from typing import List


@dataclass
class AstUser:
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    last_login: str
    auth_provider: str
    creation_date: str
    is_enabled: bool
    is_mfa_configured: bool
    roles: List[str]
    groups: List[str]
    required_actions: List[str]
    email_verified: bool


def construct_ast_user(item):
    return AstUser(
        id=item.get("id"),
        username=item.get("username"),
        first_name=item.get("firstName"),
        last_name=item.get("lastName"),
        email=item.get("email"),
        last_login=item.get("lastLogin"),
        auth_provider=item.get("authProvider"),
        creation_date=item.get("creationDate"),
        is_enabled=item.get("isEnabled"),
        is_mfa_configured=item.get("isMfaConfigured"),
        roles=item.get("roles"),
        groups=item.get("groups"),
        required_actions=item.get("requiredActions"),
        email_verified=item.get("emailVerified"),
    )
