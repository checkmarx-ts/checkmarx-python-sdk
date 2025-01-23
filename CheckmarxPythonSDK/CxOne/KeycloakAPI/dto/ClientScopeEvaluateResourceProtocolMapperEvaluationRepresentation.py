class ClientScopeEvaluateResourceProtocolMapperEvaluationRepresentation:
    def __init__(self, container_id, container_name, container_type, mapper_id, mapper_name, protocol_mapper):
        self.containerId = container_id
        self.containerName = container_name
        self.containerType = container_type
        self.mapperId = mapper_id
        self.mapperName = mapper_name
        self.protocolMapper = protocol_mapper

    def __str__(self):
        return f"ClientScopeEvaluateResourceProtocolMapperEvaluationRepresentation(" \
               f"containerId={self.containerId} " \
               f"containerName={self.containerName} " \
               f"containerType={self.containerType} " \
               f"mapperId={self.mapperId} " \
               f"mapperName={self.mapperName} " \
               f"protocolMapper={self.protocolMapper} " \
               f")"

    def to_dict(self):
        return {
            "containerId": self.containerId,
            "containerName": self.containerName,
            "containerType": self.containerType,
            "mapperId": self.mapperId,
            "mapperName": self.mapperName,
            "protocolMapper": self.protocolMapper,
        }


def construct_client_scope_evaluate_resource_protocol_mapper_evaluation_representation(item):
    return ClientScopeEvaluateResourceProtocolMapperEvaluationRepresentation(
        container_id=item.get("containerId"),
        container_name=item.get("containerName"),
        container_type=item.get("containerType"),
        mapper_id=item.get("mapperId"),
        mapper_name=item.get("mapperName"),
        protocol_mapper=item.get("protocolMapper"),
    )
