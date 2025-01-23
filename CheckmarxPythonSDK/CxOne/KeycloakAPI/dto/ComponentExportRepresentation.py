class ComponentExportRepresentation:
    def __init__(self, config, component_export_representation_id, name, provider_id, sub_components, sub_type):
        self.config = config
        self.id = component_export_representation_id
        self.name = name
        self.providerId = provider_id
        self.subComponents = sub_components
        self.subType = sub_type

    def __str__(self):
        return f"ComponentExportRepresentation(" \
               f"config={self.config} " \
               f"id={self.id} " \
               f"name={self.name} " \
               f"providerId={self.providerId} " \
               f"subComponents={self.subComponents} " \
               f"subType={self.subType} " \
               f")"

    def to_dict(self):
        return {
            "config": self.config,
            "id": self.id,
            "name": self.name,
            "providerId": self.providerId,
            "subComponents": self.subComponents,
            "subType": self.subType,
        }


def construct_component_export_representation(item):
    return ComponentExportRepresentation(
        config=item.get("config"),
        component_export_representation_id=item.get("id"),
        name=item.get("name"),
        provider_id=item.get("providerId"),
        sub_components=item.get("subComponents"),
        sub_type=item.get("subType"),
    )
