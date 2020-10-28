# encoding: utf-8


class Team(object):

    def __init__(self, team_id, name, full_name, parent_id):
        """

        Args:
            team_id (int):
            name (str):
            full_name (str):
            parent_id (int):
        """

        self.id = team_id
        self.name = name
        self.full_name = full_name
        self.parent_id = parent_id

    def __str__(self):
        return """Team(id={}, name={}, full_name={}, parent_id={})""".format(
            self.id, self.name, self.full_name, self.parent_id
        )
