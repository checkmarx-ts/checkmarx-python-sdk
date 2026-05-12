from dataclasses import dataclass


@dataclass
class ClientProfilesRepresentation:
    global_profiles: ... = None
    profiles: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientProfilesRepresentation":
        return cls(
            global_profiles=item.get("globalProfiles"),
            profiles=item.get("profiles"),
        )
