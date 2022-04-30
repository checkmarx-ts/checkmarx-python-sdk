class Queries(object):
    def __init__(self, name, group, level, lang, path, modify, is_executable):
        """

        Args:
            name (str):
            group (str):
            level (str):
            lang (str):
            path (str):
            modify (str):
            is_executable (bool):
        """
        self.name = name
        self.group = group
        self.level = level
        self.lang = lang
        self.path = path
        self.modify = modify
        self.isExecutable = is_executable

    def __str__(self):
        return """Queries(name={}, group={}, level={}, lang={}, path={}, modify={}, isExecutable={})""".format(
            self.name, self.group, self.level, self.lang, self.path, self.modify, self.isExecutable
        )
