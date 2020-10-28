# encoding: utf-8


class CxPreset(object):
    """
    the queries set
    """

    def __init__(self, preset_id, name=None, owner_name=None, link=None, query_ids=None):
        """

        Args:
            preset_id (int):
            name (str):
            owner_name (str):
            link (:obj:`CxLink`):
            query_ids(:obj:`list` of :obj:`int`):
        """
        self.id = preset_id
        self.name = name
        self.owner_name = owner_name
        self.link = link
        self.query_ids = query_ids

    def __str__(self):
        return "CxPreset(id={}, name={}, owner_name={}, link={}, query_ids={})".format(
            self.id, self.name, self.owner_name, self.link, self.query_ids
        )
