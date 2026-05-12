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
