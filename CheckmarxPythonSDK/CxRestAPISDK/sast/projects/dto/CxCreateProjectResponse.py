# encoding: utf-8


class CxCreateProjectResponse(object):
    """
    the response data, when create a project
    """
    def __init__(self, project_id, link):
        """

        Args:
            project_id (int):
            link (:obj:`CxLink`):
        """
        self.id = project_id
        self.link = link

    def __str__(self):
        return "CxCreateProjectResponse(id={}, link={})".format(self.id, self.link)
