# encoding: utf-8


class LDAPGroup(object):

    def __init__(self, name, dn):
        """

        Args:
            name (str):
            dn (str):
        """
        self.name = name
        self.dn = dn

    def __str__(self):
        return """LDAPGroup(name={}, dn={})""".format(self.name, self.dn)
