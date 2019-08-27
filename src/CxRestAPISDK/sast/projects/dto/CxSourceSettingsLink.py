# encoding: utf-8


class CxSourceSettingsLink(object):
    """
    source settings link
    """

    def __init__(self, source_settings_link_type, rel, uri):
        """

        Args:
            source_settings_link_type (str):
            rel (str):
            uri (str):
        """
        self.type = source_settings_link_type
        self.rel = rel
        self.uri = uri

    def __str__(self):
        return "CxSourceSettingsLink(source_settings_link_type={}, rel={}, uri={})".format(
            self.type, self.rel, self.uri
        )
