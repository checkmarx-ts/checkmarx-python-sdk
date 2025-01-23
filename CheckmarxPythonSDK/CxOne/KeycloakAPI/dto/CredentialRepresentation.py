class CredentialRepresentation:
    def __init__(self, created_date, credential_data, credential_representation_id, priority, secret_data, temporary,
                 credential_representation_type, user_label, value):
        self.createdDate = created_date
        self.credentialData = credential_data
        self.id = credential_representation_id
        self.priority = priority
        self.secretData = secret_data
        self.temporary = temporary
        self.type = credential_representation_type
        self.userLabel = user_label
        self.value = value

    def __str__(self):
        return f"CredentialRepresentation(" \
               f"createdDate={self.createdDate} " \
               f"credentialData={self.credentialData} " \
               f"id={self.id} " \
               f"priority={self.priority} " \
               f"secretData={self.secretData} " \
               f"temporary={self.temporary} " \
               f"type={self.type} " \
               f"userLabel={self.userLabel} " \
               f"value={self.value} " \
               f")"

    def to_dict(self):
        return {
            "createdDate": self.createdDate,
            "credentialData": self.credentialData,
            "id": self.id,
            "priority": self.priority,
            "secretData": self.secretData,
            "temporary": self.temporary,
            "type": self.type,
            "userLabel": self.userLabel,
            "value": self.value,
        }


def construct_credential_representation(item):
    return CredentialRepresentation(
        created_date=item.get("createdDate"),
        credential_data=item.get("credentialData"),
        credential_representation_id=item.get("id"),
        priority=item.get("priority"),
        secret_data=item.get("secretData"),
        temporary=item.get("temporary"),
        credential_representation_type=item.get("type"),
        user_label=item.get("userLabel"),
        value=item.get("value"),
    )
