from dataclasses import dataclass


@dataclass
class UserProfileAttributeGroupMetadata:
    name: str
    display_header: str
    display_description: str
    annotations: dict

    def to_dict(self):
        return {
            "name": self.name,
            "displayHeader": self.display_header,
            "displayDescription": self.display_description,
            "annotations": self.annotations,
        }


def construct_user_profile_attribute_group_metadata(item):
    return UserProfileAttributeGroupMetadata(
        name=item.get("name"),
        display_header=item.get("displayHeader"),
        display_description=item.get("displayDescription"),
        annotations=item.get("annotations"),
    )
