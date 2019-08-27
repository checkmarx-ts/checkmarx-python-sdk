# encoding: utf-8

from pathlib import Path


class CxTeam(object):
    """
    The team.
    """
    def __init__(self, team_id=None, name=None, full_name=None, parent_id=None):
        """

        Args:
            team_id (int): team id is unique at global level
            name (str): the name after last slash in the full name, this name is not unique at global level.
            full_name (str): team full name, for example: "/CxServer/SP/Company/Users",
                team full name is unique at global level
                default team full names:
                '/CxServer'
                '/CxServer/SP'
                '/CxServer/SP/Company'
                '/CxServer/SP/Company/Users'
            parent_id (int):
        """
        self.team_id = team_id
        self.name = name
        self.full_name = Path(full_name)
        self.parent_id = parent_id

    def __str__(self):
        return "CxTeam(team_id={}, name={}, full_name={}, parent_id={})".format(
            self.team_id, self.name, self.full_name, self.parent_id
        )
