from dataclasses import dataclass


@dataclass
class UserProfileAttributeMetadata:
    name: str
    display_name: str
    required: bool
    read_only: bool
    annotations: dict
    validators: dict
    group: str
