class ServerInfoRepresentation:
    def __init__(self, builtin_protocol_mappers, client_importers, client_installations, component_types, enums,
                 identity_providers, memory_info, password_policies, profile_info, protocol_mapper_types, providers,
                 social_providers, system_info, themes):
        self.builtinProtocolMappers = builtin_protocol_mappers
        self.clientImporters = client_importers
        self.clientInstallations = client_installations
        self.componentTypes = component_types
        self.enums = enums
        self.identityProviders = identity_providers
        self.memoryInfo = memory_info
        self.passwordPolicies = password_policies
        self.profileInfo = profile_info
        self.protocolMapperTypes = protocol_mapper_types
        self.providers = providers
        self.socialProviders = social_providers
        self.systemInfo = system_info
        self.themes = themes

    def __str__(self):
        return f"ServerInfoRepresentation(" \
               f"builtinProtocolMappers={self.builtinProtocolMappers} " \
               f"clientImporters={self.clientImporters} " \
               f"clientInstallations={self.clientInstallations} " \
               f"componentTypes={self.componentTypes} " \
               f"enums={self.enums} " \
               f"identityProviders={self.identityProviders} " \
               f"memoryInfo={self.memoryInfo} " \
               f"passwordPolicies={self.passwordPolicies} " \
               f"profileInfo={self.profileInfo} " \
               f"protocolMapperTypes={self.protocolMapperTypes} " \
               f"providers={self.providers} " \
               f"socialProviders={self.socialProviders} " \
               f"systemInfo={self.systemInfo} " \
               f"themes={self.themes} " \
               f")"

    def to_dict(self):
        return {
            "builtinProtocolMappers": self.builtinProtocolMappers,
            "clientImporters": self.clientImporters,
            "clientInstallations": self.clientInstallations,
            "componentTypes": self.componentTypes,
            "enums": self.enums,
            "identityProviders": self.identityProviders,
            "memoryInfo": self.memoryInfo,
            "passwordPolicies": self.passwordPolicies,
            "profileInfo": self.profileInfo,
            "protocolMapperTypes": self.protocolMapperTypes,
            "providers": self.providers,
            "socialProviders": self.socialProviders,
            "systemInfo": self.systemInfo,
            "themes": self.themes,
        }


def construct_server_info_representation(item):
    return ServerInfoRepresentation(
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
