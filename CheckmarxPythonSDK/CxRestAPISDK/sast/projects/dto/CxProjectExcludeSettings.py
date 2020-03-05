# encoding: utf-8


class CxProjectExcludeSettings(object):
    """
    project exclude settings
    """

    def __init__(self, project_id, exclude_folders_pattern, exclude_files_pattern, link):
        """

        Args:
            project_id (int):
            exclude_folders_pattern (str):
            exclude_files_pattern (str):
            link (:obj:`CxLink`):
        """
        self.project_id = project_id
        self.exclude_folders_pattern = exclude_folders_pattern
        self.exclude_files_pattern = exclude_files_pattern
        self.link = link

    def __str__(self):
        return """CxProjectExcludeSettings(project_id={}, exclude_folders_pattern={}, 
        exclude_files_pattern={}, link={})""".format(
            self.project_id, self.exclude_folders_pattern, self.exclude_files_pattern, self.link
        )
