from dataclasses import dataclass


@dataclass
class ServerInfoRepresentation:
    builtin_protocol_mappers: ... = None
    client_importers: ... = None
    client_installations: ... = None
    component_types: ... = None
    enums: ... = None
    identity_providers: ... = None
    memory_info: ... = None
    password_policies: ... = None
    profile_info: ... = None
    protocol_mapper_types: ... = None
    providers: ... = None
    social_providers: ... = None
    system_info: ... = None
    themes: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ServerInfoRepresentation":
        return cls(
            builtin_protocol_mappers=item.get("builtinProtocolMappers"),
            client_importers=item.get("clientImporters"),
            client_installations=item.get("clientInstallations"),
            component_types=item.get("componentTypes"),
            enums=item.get("enums"),
            identity_providers=item.get("identityProviders"),
            memory_info=item.get("memoryInfo"),
            password_policies=item.get("passwordPolicies"),
            profile_info=item.get("profileInfo"),
            protocol_mapper_types=item.get("protocolMapperTypes"),
            providers=item.get("providers"),
            social_providers=item.get("socialProviders"),
            system_info=item.get("systemInfo"),
            themes=item.get("themes"),
        )
