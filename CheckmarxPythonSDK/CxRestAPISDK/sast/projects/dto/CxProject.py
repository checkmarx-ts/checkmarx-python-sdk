# encoding: utf-8


class CxProject(object):
    """
    the project details
    """

    def __init__(self, project_id=None, team_id=None, name=None, is_public=None, source_settings_link=None, link=None,
                 custom_fields=None, links=None, project_queue_settings=None):
        """

        Args:
            project_id (int):
            team_id (str):
            name (str):
            is_public (boolean):
            source_settings_link (:obj:`CxSourceSettingsLink`):
            link (:obj:`CxLink`):
            custom_fields (`list` of `CxCustomFields`):
            links ( `list` of `CxLink`)
            project_queue_settings (`CxProjectQueueSetting`)
        """
        self.project_id = project_id
        self.team_id = team_id
        self.name = name
        self.is_public = is_public
        self.source_settings_link = source_settings_link
        self.link = link
        self.custom_fields = custom_fields
        self.links = links
        self.project_queue_settings = project_queue_settings

    def __str__(self):
        return """CxProject(project_id={}, team_id={}, name={}, 
                is_public={}, source_settings_link={}, link={}, customFields={}, 
                links={}, project_queue_settings={})""".format(
            self.project_id, self.team_id, self.name, self.is_public, self.source_settings_link, self.link,
            self.custom_fields, self.links, self.project_queue_settings
        )
