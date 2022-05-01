class MethodParameter(object):
    def __init__(self, name, label, documentation):
        """

        Args:
            name (str):
            label (str):
            documentation (str):
        """
        self.name = name
        self.label = label
        self.documentation = documentation

    def __str__(self):
        return """MethodParameter(name={}, label={}, documentation={})""".format(
            self.name, self.label, self.documentation
        )
