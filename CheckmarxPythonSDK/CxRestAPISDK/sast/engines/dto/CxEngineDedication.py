class CxEngineDedication(object):

    def __init__(self, item_type, item_id, item_name=None, is_deprecated=None):
        """

        Args:
            item_type (str): ['Scan', 'Project', 'Team']
            item_id (str): corresponding to the id of item_type, such as ScanId, ProjectId, TeamId
            item_name (str):
            is_deprecated (bool):
        """
        if item_type not in ['Scan', 'Project', 'Team']:
            raise ValueError("parameter item_type should be one of member from list ['Scan', 'Project', 'Team']")

        self.item_type = item_type
        self.item_id = item_id
        self.item_name = item_name
        self.is_deprecated = is_deprecated

    def __str__(self):
        return """CxEngineDedication(item_type={}, item_id={}, item_name={}, is_deprecated={})""".format(
            self.item_type, self.item_id, self.item_name, self.is_deprecated
        )

    def to_dict(self):
        return {
            "itemType": self.item_type,
            "itemId": self.item_id,
        }
