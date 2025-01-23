class ClientProfilesRepresentation:
    def __init__(self, global_profiles, profiles):
        self.globalProfiles = global_profiles
        self.profiles = profiles

    def __str__(self):
        return f"ClientProfilesRepresentation(" \
               f"globalProfiles={self.globalProfiles} " \
               f"profiles={self.profiles} " \
               f")"

    def to_dict(self):
        return {
            "globalProfiles": self.globalProfiles,
            "profiles": self.profiles,
        }


def construct_client_profiles_representation(item):
    return ClientProfilesRepresentation(
        global_profiles=item.get("globalProfiles"),
        profiles=item.get("profiles"),
    )
