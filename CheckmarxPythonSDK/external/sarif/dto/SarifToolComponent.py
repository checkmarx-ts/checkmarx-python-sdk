class SarifToolComponent:
    def __init__(self, name, guid, index):
        """

        Args:
            name (str):
            guid (str):
            index (int):
        """
        self.name = name
        self.guid = guid
        self.index = index

    def __str__(self):
        return f"SarifToolComponent(" \
               f"name={self.name}, "\
               f"guid={self.guid}, "\
               f"index={self.index}"\
               f")"
