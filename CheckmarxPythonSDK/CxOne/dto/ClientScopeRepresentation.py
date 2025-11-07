class ClientScopeRepresentation:
    def __init__(self, attributes, description, client_scope_representation_id, name, protocol, protocol_mappers):
        self.attributes = attributes
        self.description = description
        self.id = client_scope_representation_id
        self.name = name
        self.protocol = protocol
        self.protocolMappers = protocol_mappers

    def __str__(self):
        return f"ClientScopeRepresentation(" \
               f"attributes={self.attributes} " \
               f"description={self.description} " \
               f"id={self.id} " \
               f"name={self.name} " \
               f"protocol={self.protocol} " \
               f"protocolMappers={self.protocolMappers} " \
               f")"

    def to_dict(self):
        return {
            "attributes": self.attributes,
            "description": self.description,
            "id": self.id,
            "name": self.name,
            "protocol": self.protocol,
            "protocolMappers": self.protocolMappers,
        }


def construct_client_scope_representation(item):
    return ClientScopeRepresentation(
        attributes=item.get("attributes"),
        description=item.get("description"),
        client_scope_representation_id=item.get("id"),
        name=item.get("name"),
        protocol=item.get("protocol"),
        protocol_mappers=item.get("protocolMappers"),
    )
