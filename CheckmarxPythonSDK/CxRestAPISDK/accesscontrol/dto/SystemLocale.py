# encoding: utf-8


class SystemLocale(object):

    def __init__(self, system_locale_id, lcid, code, display_name):
        """

        Args:
            system_locale_id (int):
            lcid (int):
            code (str):
            display_name (str):
        """
        self.id = int(system_locale_id)
        self.lcid = int(lcid)
        self.code = code
        self.display_name = display_name

    def __str__(self):
        return """SystemLocale(id={}, lcid={}, code={}, display_name={})""".format(
            self.id, self.lcid, self.code, self.display_name
        )
