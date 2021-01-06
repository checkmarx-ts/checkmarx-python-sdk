# encoding: utf-8


class CxCustomField(object):
    """
    custom fields
    """

    def __init__(self, custom_field_id, name, value=None):
        """

        Args:
            custom_field_id (int):
            name (str):
            value (str):
        """
        self.id = custom_field_id
        self.name = name
        self.value = value

    def __str__(self):
        return "custom_fields(id={}, name={}, value={})".format(
            self.id, self.name, self.value
        )
