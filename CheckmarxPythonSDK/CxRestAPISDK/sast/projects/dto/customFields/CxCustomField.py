# encoding: utf-8


class CxCustomField(object):
    """
    custom fields
    """

    def __init__(self, custom_field_id, name, value=None, is_mandatory=None, project_id=None):
        """

        Args:
            custom_field_id (int):
            name (str):
            value (str):
        """
        self.id = custom_field_id
        self.name = name
        self.value = value
        self.is_mandatory = is_mandatory
        self.project_id = project_id

    def __str__(self):
        return "custom_fields(id={}, name={}, value={}, is_mandatory={}, project_id={})".format(
            self.id, self.name, self.value, self.is_mandatory, self.project_id
        )

    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
        }
