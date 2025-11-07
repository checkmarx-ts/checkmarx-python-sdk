from dataclasses import dataclass


@dataclass
class RoleRepresentationComposites:
    client: str
    realm: str

    def to_dict(self):
        return {
            "client": self.client,
            "realm": self.realm,
        }


def construct_role_representation_composites(item):
    return RoleRepresentationComposites(
        client=item.get("client"),
        realm=item.get("realm"),
    )
