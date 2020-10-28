# encoding: utf-8


class CxCustomField(object):
    """
    custom fields
    """

    def __init__(self, custom_field_id, name):
        """

        Args:
            custom_field_id (int):
            name (str):
        """
        self.id = custom_field_id
        self.name = name

    def __str__(self):
        return "custom_fields(id={}, name={})".format(
            self.id, self.name
        )
