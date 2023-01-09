class SarifRegion:
    def __init__(self, start_line, start_column, end_column):
        """

        Args:
            start_line (int):
            start_column (int):
            end_column (int):
        """
        self.StartLine = start_line
        self.StartColumn = start_column
        self.EndColumn = end_column

    def __str__(self):
        return f"SarifRegion(" \
               f"start_line={self.StartLine}, "\
               f"start_column={self.StartColumn}, "\
               f"end_column={self.EndColumn}" \
               f")"
