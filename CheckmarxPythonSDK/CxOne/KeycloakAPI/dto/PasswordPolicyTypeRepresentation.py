class PasswordPolicyTypeRepresentation:
    def __init__(self, config_type, default_value, display_name, password_policy_type_representation_id,
                 multiple_supported):
        self.configType = config_type
        self.defaultValue = default_value
        self.displayName = display_name
        self.id = password_policy_type_representation_id
        self.multipleSupported = multiple_supported

    def __str__(self):
        return f"PasswordPolicyTypeRepresentation(" \
               f"configType={self.configType} " \
               f"defaultValue={self.defaultValue} " \
               f"displayName={self.displayName} " \
               f"id={self.id} " \
               f"multipleSupported={self.multipleSupported} " \
               f")"

    def to_dict(self):
        return {
            "configType": self.configType,
            "defaultValue": self.defaultValue,
            "displayName": self.displayName,
            "id": self.id,
            "multipleSupported": self.multipleSupported,
        }


def construct_password_policy_type_representation(item):
    return PasswordPolicyTypeRepresentation(
        config_type=item.get("configType"),
        default_value=item.get("defaultValue"),
        display_name=item.get("displayName"),
        password_policy_type_representation_id=item.get("id"),
        multiple_supported=item.get("multipleSupported"),
    )
