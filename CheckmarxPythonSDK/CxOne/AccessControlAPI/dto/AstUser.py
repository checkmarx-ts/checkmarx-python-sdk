from dataclasses import dataclass
from typing import List


@dataclass
class AstUser:
    """

    Attributes:
        user_id (str):
        username (str):
        first_name (str):
        last_name (str):
        email (str):
        last_login (str):
        roles (List[str]):
        groups (List[str]):
    """
    user_id: str
    username: str
    first_name: str
    last_name: str
    email: str
    last_login: str
    roles: List[str]
    groups: List[str]


def construct_ast_user(item):
    return AstUser(
        user_id=item.get("id"),
        username=item.get("username"),
        first_name=item.get("firstName"),
        last_name=item.get("lastName"),
        email=item.get("email"),
        last_login=item.get("lastLogin"),
        roles=item.get("roles"),
        groups=item.get("groups")
    )
