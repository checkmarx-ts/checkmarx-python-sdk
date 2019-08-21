# encoding: utf-8


class CxCreateProjectResponse(object):
    """
    the response data, when create a project
    """
    def __init__(self, project_id, link):
        """

        """
        self.id = project_id
        self.link = link
