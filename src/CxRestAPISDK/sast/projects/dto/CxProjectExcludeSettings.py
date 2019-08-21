# encoding: utf-8


class CxProjectExcludeSettings(object):
    """
    project exclude settings
    """

    def __init__(self, project_id, exclude_folders_pattern, exclude_files_pattern, link):
        """

        :param project_id: int
        :param exclude_folders_pattern: str
        :param exclude_files_pattern: str
        :param link: CxLink.CxLink
        """
        self.project_id = project_id
        self.exclude_folders_pattern = exclude_folders_pattern
        self.exclude_files_pattern = exclude_files_pattern
        self.link = link
