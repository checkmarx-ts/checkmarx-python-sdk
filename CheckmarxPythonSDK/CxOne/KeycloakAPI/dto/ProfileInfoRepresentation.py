class ProfileInfoRepresentation:
    def __init__(self, disabled_features, experimental_features, name, preview_features):
        self.disabledFeatures = disabled_features
        self.experimentalFeatures = experimental_features
        self.name = name
        self.previewFeatures = preview_features

    def __str__(self):
        return f"ProfileInfoRepresentation(" \
               f"disabledFeatures={self.disabledFeatures} " \
               f"experimentalFeatures={self.experimentalFeatures} " \
               f"name={self.name} " \
               f"previewFeatures={self.previewFeatures} " \
               f")"

    def to_dict(self):
        return {
            "disabledFeatures": self.disabledFeatures,
            "experimentalFeatures": self.experimentalFeatures,
            "name": self.name,
            "previewFeatures": self.previewFeatures,
        }


def construct_profile_info_representation(item):
    return ProfileInfoRepresentation(
        disabled_features=item.get("disabledFeatures"),
        experimental_features=item.get("experimentalFeatures"),
        name=item.get("name"),
        preview_features=item.get("previewFeatures"),
    )
