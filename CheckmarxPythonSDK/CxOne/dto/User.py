from dataclasses import dataclass
from typing import List


@dataclass
class User:
    id: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
    email_verified: bool = None
    enabled: bool = None
    groups: List[str] = None
    roles: List[str] = None
    required_actions: List[str] = None
    created_timestamp: int = None


def construct_user(item):
    return User(
        id=item.get("id"),
        username=item.get("username"),
        first_name=item.get("firstName"),
        last_name=item.get("lastName"),
        email=item.get("email"),
        email_verified=item.get("emailVerified"),
        enabled=item.get("enabled"),
        groups=item.get("groups"),
        roles=item.get("roles"),
        required_actions=item.get("requiredActions"),
        created_timestamp=item.get("createdTimestamp"),
    )
