from dataclasses import dataclass


@dataclass
class SocialLinkRepresentation:
    social_provider: str
    social_user_id: str
    social_username: str
