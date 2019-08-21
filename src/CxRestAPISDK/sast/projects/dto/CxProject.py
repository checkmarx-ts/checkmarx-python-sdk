# encoding: utf-8


class CxProject(object):
    """
    the project details
    """

    def __init__(self, project_id=None, team_id=None, name=None, is_public=None, source_settings_link=None, link=None):
        """
        :param project_id: int
        :param team_id: str
        :param name: str
        :param is_public: boolean
        :param source_settings_link: CxSourceSettingsLink
        :param link: CxLink
        """
        self.project_id = project_id
        self.team_id = team_id
        self.name = name
        self.is_public = is_public
        self.source_settings_link = source_settings_link
        self.link = link
