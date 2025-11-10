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

    def to_dict(self):
        return {
            "name": self.name,
            "displayName": self.display_name,
            "required": self.required,
            "readOnly": self.read_only,
            "annotations": self.annotations,
            "validators": self.validators,
            "group": self.group,
        }


def construct_user_profile_attribute_metadata(item):
    return UserProfileAttributeMetadata(
        name=item.get("name"),
        display_name=item.get("displayName"),
        required=item.get("required"),
        read_only=item.get("readOnly"),
        annotations=item.get("annotations"),
        validators=item.get("validators"),
        group=item.get("group"),
    )
