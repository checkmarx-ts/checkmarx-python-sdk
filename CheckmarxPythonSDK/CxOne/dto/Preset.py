class Preset(object):
    def __init__(self, preset_id=None, name=None, description=None, custom=None, query_ids=None):
        """

        Args:
            preset_id (int):
            name (str):
        """
        self.id = preset_id
        self.name = name
        self.description = description
        self.custom = custom
        self.query_ids = query_ids

    def __str__(self):
        return f"""Preset(
        id={self.id}, 
        name={self.name},
        description={self.description},
        custom={self.custom},
        query_ids={self.query_ids},
        )"""
