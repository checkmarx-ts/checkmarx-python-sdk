from dataclasses import dataclass


@dataclass
class UserProfileAttributeGroupMetadata:
    name: str
    display_header: str
    display_description: str
    annotations: dict
