from dataclasses import dataclass


@dataclass
class InternalUser:
    id: str = None
    username: str = None
    first_name: str = None
    last_name: str = None


def construct_internal_user(item):
    return InternalUser(
        id=item.get("id"),
        username=item.get("username"),
        first_name=item.get("firstName"),
        last_name=item.get("lastName"),
    )
