# encoding: utf-8

import json


class CxCreateProjectRequest(object):
    """
    the data type used to create a project.
    """

    def __init__(self, name, team_id, is_public):
        """

        Args:
            name (str):
            team_id (int):
            is_public (boolean):
        """
        self.name = name
        self.owning_team = team_id
        self.is_public = is_public

    def get_post_data(self):
        """
        get the data that will be posted to create a project with default configuration.
        :return:
            str
        """
        return json.dumps(
            {
                "name": self.name,
                "owningTeam": self.owning_team,
                "isPublic": self.is_public
            }
        )

    def __str__(self):
        return "CxCreateProjectRequest(name={}, owning_team={}, is_public={})".format(
            self.name, self.owning_team, self.is_public
        )
