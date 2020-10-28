# encoding: utf-8


class CxTeam(object):
    """
    The team.
    """
    def __init__(self, team_id=None, name=None, full_name=None, parent_id=None):
        """

        Args:
            team_id (int, str): team id is unique at global level.
                                        From v9.0, team id changes to integer
            name (str): the name after last slash in the full name, this name is not unique at global level.
            full_name (str): team full name.
                from v9.0, team full name change to linux file path style, used to be windows style
                for example: "/CxServer/SP/Company/Users",
                team full name is unique at global level
                default team full names:
                '/CxServer'
                '/CxServer/SP'
                '/CxServer/SP/Company'
                '/CxServer/SP/Company/Users'
            parent_id (int, str):
        """
        self.team_id = team_id
        self.name = name
        self.full_name = full_name.replace("\\", "/")
        self.parent_id = parent_id

    def __str__(self):
        return "CxTeam(team_id={}, name={}, full_name={}, parent_id={})".format(
            self.team_id, self.name, self.full_name, self.parent_id
        )
