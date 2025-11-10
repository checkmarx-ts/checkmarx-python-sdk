from dataclasses import dataclass


@dataclass
class SocialLinkRepresentation:
    social_provider: str
    social_user_id: str
    social_username: str

    def to_dict(self):
        return {
            "socialProvider": self.social_provider,
            "socialUserId": self.social_user_id,
            "socialUsername": self.social_username,
        }


def construct_social_link_representation(item):
    return SocialLinkRepresentation(
        social_provider=item.get("socialProvider"),
        social_user_id=item.get("socialUserId"),
        social_username=item.get("socialUsername"),
    )
