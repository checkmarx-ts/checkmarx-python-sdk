class User(object):
    def __init__(self, user_id, created_timestamp, username, enabled, totp, email_verified, first_name, last_name,
                 email, attributes, disableable_credential_types, required_actions, not_before, access):
        self.id = user_id
        self.createdTimestamp = created_timestamp
        self.username = username
        self.enabled = enabled
        self.totp = totp
        self.emailVerified = email_verified
        self.firstName = first_name
        self.lastName = last_name
        self.email = email
        self.attributes = attributes
        self.disableableCredentialTypes = disableable_credential_types
        self.requiredActions = required_actions
        self.notBefore = not_before
        self.access = access

    def __str__(self):
        return f"User(" \
               f"id={self.id}, " \
               f"createdTimestamp={self.createdTimestamp}, " \
               f"username={self.username}, " \
               f"enabled={self.enabled}, " \
               f"totp={self.totp}, " \
               f"emailVerified={self.emailVerified}, " \
               f"firstName={self.firstName}, " \
               f"lastName={self.lastName}, " \
               f"email={self.email}, " \
               f"attributes={self.attributes}, " \
               f"disableableCredentialTypes={self.disableableCredentialTypes}, " \
               f"requiredActions={self.requiredActions}, " \
               f"notBefore={self.notBefore}, " \
               f"access={self.access}" \
               f")"


def construct_user(item):
    return User(
        user_id=item.get("id"),
        created_timestamp=item.get("createdTimestamp"),
        username=item.get("username"),
        enabled=item.get("enabled"),
        totp=item.get("totp"),
        email_verified=item.get("emailVerified"),
        first_name=item.get("firstName"),
        last_name=item.get("lastName"),
        email=item.get("email"),
        attributes=item.get("attributes"),
        disableable_credential_types=item.get("disableableCredentialTypes"),
        required_actions=item.get("requiredActions"),
        not_before=item.get("notBefore"),
        access=item.get("access"),
    )
