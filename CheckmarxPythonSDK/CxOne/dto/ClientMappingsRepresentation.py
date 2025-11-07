class ClientMappingsRepresentation:
    def __init__(self, client, client_mappings_representation_id, mappings):
        self.client = client
        self.id = client_mappings_representation_id
        self.mappings = mappings

    def __str__(self):
        return f"ClientMappingsRepresentation(" \
               f"client={self.client} " \
               f"id={self.id} " \
               f"mappings={self.mappings} " \
               f")"

    def to_dict(self):
        return {
            "client": self.client,
            "id": self.id,
            "mappings": self.mappings,
        }


def construct_client_mappings_representation(item):
    return ClientMappingsRepresentation(
        client=item.get("client"),
        client_mappings_representation_id=item.get("id"),
        mappings=item.get("mappings"),
    )
