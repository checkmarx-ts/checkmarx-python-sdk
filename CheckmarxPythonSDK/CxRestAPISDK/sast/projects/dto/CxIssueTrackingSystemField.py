# encoding: utf-8


class CxIssueTrackingSystemField(object):
    """
    field
    """
    def __init__(self, tracking_system_field_id, name, multiple, required, supported, allowed_values):
        """

        Args:
            tracking_system_field_id (int):
            name (str):
            multiple (boolean):
            required (boolean):
            supported (boolean):
            allowed_values (:obj:`list` of :obj:`CxIssueTrackingSystemFieldAllowedValue`):
        """
        self.id = tracking_system_field_id
        self.name = name
        self.multiple = multiple
        self.required = required
        self.supported = supported
        self.allowed_values = allowed_values

    def __str__(self):
        return """CxIssueTrackingSystemField(id={}, name={], multiple={], required={], 
                supported={], allowed_values={})""".format(
            self.id, self.name, self.multiple, self.required, self.supported, self.allowed_values
        )
