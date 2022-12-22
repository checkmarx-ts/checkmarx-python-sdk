class AstUser:
    def __init__(self, user_id, username, first_name, last_name, email, last_login, roles, groups):
        """

        Args:
            user_id (str):
            username (str):
            first_name (str):
            last_name (str):
            email (str):
            last_login (str):
            roles (List[str]):
            groups (List[str]):
        """
        self.id = user_id
        self.username = username
        self.firstName = first_name
        self.lastName = last_name
        self.email = email
        self.lastLogin = last_login
        self.roles = roles
        self.groups = groups

    def __str__(self):
        return f"AstUser("\
               f"id={self.id}, " \
               f"username={self.username}, "\
               f"firstName={self.firstName}, " \
               f"lastName={self.lastName}, " \
               f"email={self.email}, " \
               f"lastLogin={self.lastLogin}, " \
               f"roles={self.roles}, "\
               f"groups={self.groups}, " \
               f")"


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
