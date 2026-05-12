from dataclasses import dataclass


@dataclass
class ClientScopeEvaluateResourceProtocolMapperEvaluationRepresentation:
    container_id: ... = None
    container_name: ... = None
    container_type: ... = None
    mapper_id: ... = None
    mapper_name: ... = None
    protocol_mapper: ... = None

    @classmethod
    def from_dict(
        cls, item: dict
    ) -> "ClientScopeEvaluateResourceProtocolMapperEvaluationRepresentation":
        return cls(
            container_id=item.get("containerId"),
            container_name=item.get("containerName"),
            container_type=item.get("containerType"),
            mapper_id=item.get("mapperId"),
            mapper_name=item.get("mapperName"),
            protocol_mapper=item.get("protocolMapper"),
        )
