from .Line import Line


class Snippet:
    def __init__(self, line):
        """
        Args:
            line (Line):
        """
        self.Line = line

    def __str__(self):
        return """Snippet(line={})""".format(self.Line)


def construct_snippet(line):
    return Snippet(line=line)
