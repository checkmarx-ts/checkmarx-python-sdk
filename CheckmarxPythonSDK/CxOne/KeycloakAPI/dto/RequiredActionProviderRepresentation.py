class RequiredActionProviderRepresentation:
    def __init__(self, alias, config, default_action, enabled, name, priority, provider_id):
        self.alias = alias
        self.config = config
        self.defaultAction = default_action
        self.enabled = enabled
        self.name = name
        self.priority = priority
        self.providerId = provider_id

    def __str__(self):
        return f"RequiredActionProviderRepresentation(" \
               f"alias={self.alias} " \
               f"config={self.config} " \
               f"defaultAction={self.defaultAction} " \
               f"enabled={self.enabled} " \
               f"name={self.name} " \
               f"priority={self.priority} " \
               f"providerId={self.providerId} " \
               f")"

    def to_dict(self):
        return {
            "alias": self.alias,
            "config": self.config,
            "defaultAction": self.defaultAction,
            "enabled": self.enabled,
            "name": self.name,
            "priority": self.priority,
            "providerId": self.providerId,
        }


def construct_required_action_provider_representation(item):
    return RequiredActionProviderRepresentation(
        alias=item.get("alias"),
        config=item.get("config"),
        default_action=item.get("defaultAction"),
        enabled=item.get("enabled"),
        name=item.get("name"),
        priority=item.get("priority"),
        provider_id=item.get("providerId"),
    )
