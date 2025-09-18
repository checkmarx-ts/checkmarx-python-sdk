from dataclasses import dataclass


@dataclass
class ScanParameter:
    """

     Args:
         key (str): Parameter key
         name (str): Name of the parameter
         category (str): The category to which the parameter belongs
         origin_level (str): The level on configuration in which the parameter is set
                 [ Environment, Tenant, Project, ConfigAsCode, Scan ]
         value (str): The value of the parameter
         value_type (str): Describes the type of object this parameter represents
                 [ String, List, Bool, Block, Secret ]
         value_type_params (str, optional): Describes the possible list values of a list type parameter
         allow_override (bool): Determines whether parameter can be overridden by parameters from higher levels

     """
    key: str
    name: str
    category: str
    origin_level: str
    value: str
    value_type: str
    value_type_params: str
    allow_override: bool

    def to_dict(self):
        data = {
            "key": self.key,
            "name": self.name,
            "category": self.category,
            "originLevel": self.origin_level,
            "value": self.value,
            "valueType": self.value_type,
            "allowOverride": self.allow_override,
        }
        if self.value_type == "List":
            data.update({"valueTypeParams": self.value_type_params})
        return data


def construct_scan_parameter(item):
    return ScanParameter(
        key=item.get("key"),
        name=item.get("name"),
        category=item.get("category"),
        origin_level=item.get("originLevel"),
        value=item.get("value"),
        value_type=item.get("valueType"),
        value_type_params=item.get("valueTypeParams"),
        allow_override=item.get("allowOverride"),
    )
