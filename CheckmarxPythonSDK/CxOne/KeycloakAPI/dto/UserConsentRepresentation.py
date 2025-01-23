class UserConsentRepresentation:
    def __init__(self, client_id, created_date, granted_client_scopes, last_updated_date):
        self.clientId = client_id
        self.createdDate = created_date
        self.grantedClientScopes = granted_client_scopes
        self.lastUpdatedDate = last_updated_date

    def __str__(self):
        return f"UserConsentRepresentation(" \
               f"clientId={self.clientId}, " \
               f"createdDate={self.createdDate}, " \
               f"grantedClientScopes={self.grantedClientScopes}, " \
               f"lastUpdatedDate={self.lastUpdatedDate}" \
               f")"

    def to_dict(self):
        return {
            "clientId": self.clientId,
            "createdDate": self.createdDate,
            "grantedClientScopes": self.grantedClientScopes,
            "lastUpdatedDate": self.lastUpdatedDate,
        }


def construct_user_consent_representation(item):
    return UserConsentRepresentation(
        client_id=item.get("clientId"),
        created_date=item.get("createdDate"),
        granted_client_scopes=item.get("grantedClientScopes"),
        last_updated_date=item.get("lastUpdatedDate"),
    )
