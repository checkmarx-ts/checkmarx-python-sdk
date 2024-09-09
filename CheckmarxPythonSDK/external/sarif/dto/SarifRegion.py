class SarifRegion:
    def __init__(self, start_line, start_column, end_column):
        """

        Args:
            start_line (int):
            start_column (int):
            end_column (int):
        """
        self.startLine = start_line
        self.startColumn = start_column
        self.endColumn = end_column

    def __str__(self):
        return f"SarifRegion(" \
               f"start_line={self.startLine}, "\
               f"start_column={self.startColumn}, "\
               f"end_column={self.endColumn}" \
               f")"
