class AccessTokenAuthorization:
    def __init__(self, permissions):
        self.permissions = permissions

    def __str__(self):
        return f"AccessTokenAuthorization(" \
               f"permissions={self.permissions} " \
               f")"

    def to_dict(self):
        return {
            "permissions": self.permissions,
        }


def construct_access_token_authorization(item):
    return AccessTokenAuthorization(
        permissions=item.get("permissions"),
    )
