class RolesRepresentation:
    def __init__(self, client, realm):
        self.client = client
        self.realm = realm

    def __str__(self):
        return f"RolesRepresentation(" \
               f"client={self.client} " \
               f"realm={self.realm} " \
               f")"

    def to_dict(self):
        return {
            "client": self.client,
            "realm": self.realm,
        }


def construct_roles_representation(item):
    return RolesRepresentation(
        client=item.get("client"),
        realm=item.get("realm"),
    )
