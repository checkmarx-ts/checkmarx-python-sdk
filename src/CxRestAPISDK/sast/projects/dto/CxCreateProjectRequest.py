# encoding: utf-8

import json


class CxCreateProjectRequest(object):
    """
    the data type used to create a project.
    """

    def __init__(self, name, owning_team, is_public):
        """
        :param name: str
        :param owning_team: str
        :param is_public: boolean
        """
        self.name = name
        self.owning_team = owning_team
        self.is_public = is_public

    def get_post_data(self):
        """
        get the data that will be posted to create a project with default configuration.
        :return: dict
        """
        return json.dumps(
            {
                "name": self.name,
                "owningTeam": self.owning_team,
                "isPublic": self.is_public
            }
        )
