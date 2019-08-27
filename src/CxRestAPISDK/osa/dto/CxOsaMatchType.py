# encoding: utf-8


class CxOsaMatchType(object):
    """
    match type
    """
    def __init__(self, match_type_id, name, description):
        """

        Args:
            match_type_id (int):
            name (str):
            description (str):
        """
        self.id = match_type_id
        self.name = name
        self.description = description

    def __str__(self):
        return """CxOsaMatchType(id={}, name={}, description={})""".format(
            self.id, self.name, self.description
        )
