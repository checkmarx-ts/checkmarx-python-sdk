class ScanParameter:
    def __init__(self, key, name, category, origin_level, value, value_type, value_type_params, allow_override):
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
        self.key = key
        self.name = name
        self.category = category
        self.originLevel = origin_level
        self.value = value
        self.valueType = value_type
        self.valueTypeParams = value_type_params
        self.allowOverride = allow_override

    def __str__(self):
        return f"ScanParameter(" \
               f"key={self.key} " \
               f"name={self.name} " \
               f"category={self.category} " \
               f"originLevel={self.originLevel} " \
               f"value={self.value} " \
               f"valueType={self.valueType} " \
               f"valueTypeParams={self.valueTypeParams} " \
               f"allowOverride={self.allowOverride} " \
               f")"

    def to_dict(self):
        data = {
            "key": self.key,
            "name": self.name,
            "category": self.category,
            "originLevel": self.originLevel,
            "value": self.value,
            "valueType": self.valueType,
            "allowOverride": self.allowOverride,
        }
        if self.valueType == "List":
            data.update({"valueTypeParams": self.valueTypeParams})
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
