class AccessTokenAccess:
    def __init__(self, roles, verify_caller):
        self.roles = roles
        self.verify_caller = verify_caller

    def __str__(self):
        return f"AccessTokenAccess(" \
               f"roles={self.roles} " \
               f"verify_caller={self.verify_caller} " \
               f")"

    def to_dict(self):
        return {
            "roles": self.roles,
            "verify_caller": self.verify_caller,
        }


def construct_access_token_access(item):
    return AccessTokenAccess(
        roles=item.get("roles"),
        verify_caller=item.get("verify_caller"),
    )
