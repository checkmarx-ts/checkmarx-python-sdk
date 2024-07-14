# encoding: utf-8


class CxCustomField(object):
    """
    custom fields
    """

    def __init__(self, custom_field_id, name, value=None, is_mandatory=None):
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

    def __str__(self):
        return "custom_fields(id={}, name={}, value={}, is_mandatory={})".format(
            self.id, self.name, self.value, self.is_mandatory
        )
