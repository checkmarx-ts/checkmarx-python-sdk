class ImportResults(object):

    def __init__(self, import_id):
        """

        Args:
            import_id (str):  The id of the new import
        """
        self.import_id = import_id

    def __str__(self):
        return """ImportResults(import_id={})""".format(
            self.import_id
        )

    def to_dict(self):
        return {
            "importId": self.import_id
        }
