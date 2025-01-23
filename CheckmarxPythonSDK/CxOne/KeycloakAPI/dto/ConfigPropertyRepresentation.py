class ConfigPropertyRepresentation:
    def __init__(self, default_value, help_text, label, name, options, secret, config_property_representation_type):
        self.defaultValue = default_value
        self.helpText = help_text
        self.label = label
        self.name = name
        self.options = options
        self.secret = secret
        self.type = config_property_representation_type

    def __str__(self):
        return f"ConfigPropertyRepresentation(" \
               f"defaultValue={self.defaultValue} " \
               f"helpText={self.helpText} " \
               f"label={self.label} " \
               f"name={self.name} " \
               f"options={self.options} " \
               f"secret={self.secret} " \
               f"type={self.type} " \
               f")"

    def to_dict(self):
        return {
            "defaultValue": self.defaultValue,
            "helpText": self.helpText,
            "label": self.label,
            "name": self.name,
            "options": self.options,
            "secret": self.secret,
            "type": self.type,
        }


def construct_config_property_representation(item):
    return ConfigPropertyRepresentation(
        default_value=item.get("defaultValue"),
        help_text=item.get("helpText"),
        label=item.get("label"),
        name=item.get("name"),
        options=item.get("options"),
        secret=item.get("secret"),
        config_property_representation_type=item.get("type"),
    )
