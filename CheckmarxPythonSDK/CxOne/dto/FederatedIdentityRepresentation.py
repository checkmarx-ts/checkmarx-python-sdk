class FederatedIdentityRepresentation:
    def __init__(self, identity_provider, user_id, user_name):
        self.identityProvider = identity_provider
        self.userId = user_id
        self.userName = user_name

    def __str__(self):
        return f"FederatedIdentityRepresentation(" \
               f"identityProvider={self.identityProvider} " \
               f"userId={self.userId} " \
               f"userName={self.userName} " \
               f")"

    def to_dict(self):
        return {
            "identityProvider": self.identityProvider,
            "userId": self.userId,
            "userName": self.userName,
        }


def construct_federated_identity_representation(item):
    return FederatedIdentityRepresentation(
        identity_provider=item.get("identityProvider"),
        user_id=item.get("userId"),
        user_name=item.get("userName"),
    )
