# encoding: utf-8


class CxProject(object):
    """
    the project details
    """

    def __init__(self, project_id=None, team_id=None, name=None, is_public=None, source_settings_link=None, link=None, customFields=None):
        """

        Args:
            project_id (int):
            team_id (str):
            name (str):
            is_public (boolean):
            source_settings_link (:obj:`CxSourceSettingsLink`):
            link (:obj:`CxLink`):
            customFields (array):
        """
        self.project_id = project_id
        self.team_id = team_id
        self.name = name
        self.is_public = is_public
        self.source_settings_link = source_settings_link
        self.link = link
        self.customFields = customFields

    def __str__(self):
        return """CxProject(project_id={}, team_id={}, name={}, 
                is_public={}, source_settings_link={}, link={}, customFields={})""".format(
            self.project_id, self.team_id, self.name, self.is_public, self.source_settings_link, self.link, self.customFields
        )
