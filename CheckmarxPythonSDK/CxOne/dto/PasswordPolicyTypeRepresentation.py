from dataclasses import dataclass


@dataclass
class PasswordPolicyTypeRepresentation:
    config_type: ... = None
    default_value: ... = None
    display_name: ... = None
    password_policy_type_representation_id: ... = None
    multiple_supported: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "PasswordPolicyTypeRepresentation":
        return cls(
            config_type=item.get("configType"),
            default_value=item.get("defaultValue"),
            display_name=item.get("displayName"),
            password_policy_type_representation_id=item.get("id"),
            multiple_supported=item.get("multipleSupported"),
        )
