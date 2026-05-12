from dataclasses import dataclass


@dataclass
class ProfileInfoRepresentation:
    disabled_features: ... = None
    experimental_features: ... = None
    name: ... = None
    preview_features: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ProfileInfoRepresentation":
        return cls(
            disabled_features=item.get("disabledFeatures"),
            experimental_features=item.get("experimentalFeatures"),
            name=item.get("name"),
            preview_features=item.get("previewFeatures"),
        )
