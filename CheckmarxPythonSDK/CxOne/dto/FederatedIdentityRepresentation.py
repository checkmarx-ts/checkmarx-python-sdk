from dataclasses import dataclass


@dataclass
class FederatedIdentityRepresentation:
    identity_provider: str
    user_id: str
    user_name: str

    def to_dict(self):
        return {
            "identityProvider": self.identity_provider,
            "userId": self.user_id,
            "userName": self.user_name,
        }


def construct_federated_identity_representation(item):
    return FederatedIdentityRepresentation(
        identity_provider=item.get("identityProvider"),
        user_id=item.get("userId"),
        user_name=item.get("userName"),
    )
