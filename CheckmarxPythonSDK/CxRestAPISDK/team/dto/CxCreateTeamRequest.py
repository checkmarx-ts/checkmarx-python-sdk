# encoding: utf-8

import json

class CxCreateTeamRequest(object):
    """
    the data type used to create a team.
    """

    def __init__(self, name, parent_id):
        """

        Args:
            name (str): the team's name
            parent_id (int): the team's parent team's id
        """
        self.name = name
        self.parent_id = parent_id

    def get_post_data(self):
        """
        get the data that will be posted to create a team.
        :return:
            str
        """
        return json.dumps(
            {
                "name": self.name,
                "parentId": self.parent_id
            }
        )

    def __str__(self):
        return "CxCreateTeamRequest(name={}, parent_id={})".format(
            self.name, self.parent_id
        )
