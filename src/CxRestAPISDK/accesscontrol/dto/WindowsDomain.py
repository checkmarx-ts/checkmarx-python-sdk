# encoding: utf-8


class WindowsDomain(object):

    def __init__(self, windows_domain_id, name, full_qualified_name):
        """

        Args:
            windows_domain_id (int):
            name (str):
            full_qualified_name (str):
        """
        self.id = windows_domain_id
        self.name = name
        self.full_qualified_name = full_qualified_name

    def __str__(self):
        return """WindowsDomain(id={}, name={}, full_qualified_name={})""".format(
            self.id, self.name, self.full_qualified_name
        )
