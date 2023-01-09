class SarifToolComponent:
    def __init__(self, name, guid, index):
        """

        Args:
            name (str):
            guid (str):
            index (int):
        """
        self.Name = name
        self.Guid = guid
        self.Index = index

    def __str__(self):
        return f"SarifToolComponent(" \
               f"name={self.Name}, "\
               f"guid={self.Guid}, "\
               f"index={self.Index}"\
               f")"
