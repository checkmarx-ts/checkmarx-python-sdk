from dataclasses import dataclass


@dataclass
class CredentialRepresentation:
    id: str
    type: str
    user_label: str
    created_date: int
    secret_data: str
    credential_data: str
    priority: int
    value: str
    temporary: bool
    device: str
    hashed_salted_value: str
    salt: str
    hash_iterations: int
    counter: int
    algorithm: str
    digits: int
    period: int
    config: dict

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "userLabel": self.user_label,
            "createdDate": self.created_date,
            "secretData": self.secret_data,
            "credentialData": self.credential_data,
            "priority": self.priority,
            "value": self.value,
            "temporary": self.temporary,
            "device": self.device,
            "hashedSaltedValue": self.hashed_salted_value,
            "salt": self.salt,
            "hashIterations": self.hash_iterations,
            "counter": self.counter,
            "algorithm": self.algorithm,
            "digits": self.digits,
            "period": self.period,
            "config": self.config,
        }


def construct_credential_representation(item):
    return CredentialRepresentation(
        id=item.get("id"),
        type=item.get("type"),
        user_label=item.get("userLabel"),
        created_date=item.get("createdDate"),
        secret_data=item.get("secretData"),
        credential_data=item.get("credentialData"),
        priority=item.get("priority"),
        value=item.get("value"),
        temporary=item.get("temporary"),
        device=item.get("device"),
        hashed_salted_value=item.get("hashedSaltedValue"),
        salt=item.get("salt"),
        hash_iterations=item.get("hashIterations"),
        counter=item.get("counter"),
        algorithm=item.get("algorithm"),
        digits=item.get("digits"),
        period=item.get("period"),
        config=item.get("config"),
    )
