class RoleRepresentationComposites:
    def __init__(self, client, realm):
        self.client = client
        self.realm = realm

    def __str__(self):
        return f"RoleRepresentationComposites(" \
               f"client={self.client} " \
               f"realm={self.realm} " \
               f")"

    def get_post_data(self):
        import json
        return json.dumps({
            "client": self.client,
            "realm": self.realm,
        })


def construct_role_representation_composites(item):
    return RoleRepresentationComposites(
        client=item.get("client"),
        realm=item.get("realm"),
    )
