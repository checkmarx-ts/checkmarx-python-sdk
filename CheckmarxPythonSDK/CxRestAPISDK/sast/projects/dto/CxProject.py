# encoding: utf-8


class CxProject(object):
    """
    the project details
    """

    def __init__(self, project_id=None, team_id=None, name=None, is_public=None, source_settings_link=None,
                 custom_fields=None, links=None, project_queue_settings=None, owner=None, is_deprecated=None,
                 is_branched=None, original_project_id=None, branched_on_scan_id=None, related_projects=None):
        """

        Args:
            project_id (int):
            team_id (str):
            name (str):
            is_public (boolean):
            source_settings_link (:obj:`CxSourceSettingsLink`):
            custom_fields (`list` of `CxCustomFields`):
            links ( `list` of `CxLink`)
            project_queue_settings (`CxProjectQueueSetting`)
        """
        self.project_id = project_id
        self.team_id = team_id
        self.name = name
        self.is_public = is_public
        self.source_settings_link = source_settings_link
        self.custom_fields = custom_fields
        self.links = links
        self.project_queue_settings = project_queue_settings
        self.owner = owner
        self.is_deprecated = is_deprecated
        self.is_branched = is_branched
        self.original_project_id = original_project_id
        self.branched_on_scan_id = branched_on_scan_id
        self.related_projects = related_projects

    def __str__(self):
        return """CxProject(project_id={}, team_id={}, name={}, 
                is_public={}, source_settings_link={}, customFields={}, 
                links={}, project_queue_settings={}, owner={}, is_deprecated={}, is_branched={}, 
                original_project_id={}, branched_on_scan_id={}, related_projects={})""".format(
            self.project_id, self.team_id, self.name, self.is_public, self.source_settings_link,
            self.custom_fields, self.links, self.project_queue_settings, self.owner, self.is_deprecated,
            self.is_branched, self.original_project_id, self.branched_on_scan_id, self.related_projects
        )
