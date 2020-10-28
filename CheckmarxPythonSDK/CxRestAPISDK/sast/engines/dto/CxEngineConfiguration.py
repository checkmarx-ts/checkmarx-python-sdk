# encoding: utf-8


class CxEngineConfiguration(object):
    """
    engine configuration
    """
    def __init__(self, engine_configuration_id=None, link=None, name=None):
        """

        Args:
            engine_configuration_id (int):
            link (:obj:`CxLink`):
            name (str):
        """
        self.id = engine_configuration_id
        self.link = link
        self.name = name

    def __str__(self):
        return "CxEngineConfiguration(id={}, link={}, name={})".format(
            self.id, self.link, self.name
        )
