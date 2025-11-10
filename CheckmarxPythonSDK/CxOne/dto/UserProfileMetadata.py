from dataclasses import dataclass
from typing import List
from .UserProfileAttributeMetadata import UserProfileAttributeMetadata, construct_user_profile_attribute_metadata
from .UserProfileAttributeGroupMetadata import (UserProfileAttributeGroupMetadata,
                                                construct_user_profile_attribute_group_metadata)


@dataclass
class UserProfileMetadata:
    attributes: List[UserProfileAttributeMetadata]
    groups: List[UserProfileAttributeGroupMetadata]

    def to_dict(self):
        return {
            "attributes": [attribute.to_dict() for attribute in self.attributes],
            "groups": [group.to_dict() for group in self.groups]
        }


def construct_user_profile_metadata(item):
    return UserProfileMetadata(
        attributes=[construct_user_profile_attribute_metadata(attribute) for attribute in item.get("attributes")],
        groups=[construct_user_profile_attribute_group_metadata(group) for group in item.get("groups")],
    )
