class Preset(object):
    def __init__(self, preset_id, name):
        """

        Args:
            preset_id (int):
            name (str):
        """
        self.id = preset_id
        self.name = name

    def __str__(self):
        return """Preset(id={}, name={})""".format(
            self.id, self.name
        )
