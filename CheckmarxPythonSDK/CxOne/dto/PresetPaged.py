class PresetPaged(object):

    def __init__(self, total_count, presets):
        """

        Args:
            total_count (int):
            presets (list of PresetSummary):
        """
        self.total_count = total_count
        self.presets = presets

    def __str__(self):
        return f"""PresetPaged(
        total_count={self.total_count},
        presets={self.presets}
        )"""
