class ComponentRepresentation:
    def __init__(self, config, component_representation_id, name, parent_id, provider_id, provider_type, sub_type):
        self.config = config
        self.id = component_representation_id
        self.name = name
        self.parentId = parent_id
        self.providerId = provider_id
        self.providerType = provider_type
        self.subType = sub_type

    def __str__(self):
        return f"ComponentRepresentation(" \
               f"config={self.config} " \
               f"id={self.id} " \
               f"name={self.name} " \
               f"parentId={self.parentId} " \
               f"providerId={self.providerId} " \
               f"providerType={self.providerType} " \
               f"subType={self.subType} " \
               f")"

    def to_dict(self):
        return {
            "config": self.config,
            "id": self.id,
            "name": self.name,
            "parentId": self.parentId,
            "providerId": self.providerId,
            "providerType": self.providerType,
            "subType": self.subType,
        }


def construct_component_representation(item):
    return ComponentRepresentation(
        config=item.get("config"),
        component_representation_id=item.get("id"),
        name=item.get("name"),
        parent_id=item.get("parentId"),
        provider_id=item.get("providerId"),
        provider_type=item.get("providerType"),
        sub_type=item.get("subType"),
    )
