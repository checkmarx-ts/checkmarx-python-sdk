class ProtocolMapperRepresentation:
    def __init__(self, config, protocol_mapper_representation_id, name, protocol, protocol_mapper):
        self.config = config
        self.id = protocol_mapper_representation_id
        self.name = name
        self.protocol = protocol
        self.protocolMapper = protocol_mapper

    def __str__(self):
        return f"ProtocolMapperRepresentation(" \
               f"config={self.config} " \
               f"id={self.id} " \
               f"name={self.name} " \
               f"protocol={self.protocol} " \
               f"protocolMapper={self.protocolMapper} " \
               f")"

    def to_dict(self):
        return {
            "config": self.config,
            "id": self.id,
            "name": self.name,
            "protocol": self.protocol,
            "protocolMapper": self.protocolMapper,
        }


def construct_protocol_mapper_representation(item):
    return ProtocolMapperRepresentation(
        config=item.get("config"),
        protocol_mapper_representation_id=item.get("id"),
        name=item.get("name"),
        protocol=item.get("protocol"),
        protocol_mapper=item.get("protocolMapper"),
    )
