class MappingsRepresentation:
    def __init__(self, client_mappings, realm_mappings):
        self.clientMappings = client_mappings
        self.realmMappings = realm_mappings

    def __str__(self):
        return f"MappingsRepresentation(" \
               f"clientMappings={self.clientMappings} " \
               f"realmMappings={self.realmMappings} " \
               f")"

    def to_dict(self):
        return {
            "clientMappings": self.clientMappings,
            "realmMappings": self.realmMappings,
        }


def construct_mappings_representation(item):
    return MappingsRepresentation(
        client_mappings=item.get("clientMappings"),
        realm_mappings=item.get("realmMappings"),
    )
