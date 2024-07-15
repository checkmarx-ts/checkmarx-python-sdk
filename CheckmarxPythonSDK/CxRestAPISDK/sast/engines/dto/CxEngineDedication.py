class CxEngineDedication(object):

    def __init__(self, item_type, item_id, item_name, is_deprecated=None):
        """

        Args:
            item_type (str):
            item_id (str):
            item_name (str):
            is_deprecated (bool):
        """
        self.item_type = item_type
        self.item_id = item_id
        self.item_name = item_name
        self.is_deprecated = is_deprecated

    def __str__(self):
        return """CxEngineDedication(item_type={}, item_id={}, item_name={}, is_deprecated={})""".format(
            self.item_type, self.item_id, self.item_name, self.is_deprecated
        )
