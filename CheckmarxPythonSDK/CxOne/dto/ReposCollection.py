# encoding: utf-8
class ReposCollection(object):
    def __init__(self, total_count, repos):
        """

        Args:
            total_count (int): The number of total records
            repos: The repositories returned within this org
        """
        self.totalCount = total_count
        self.repos = repos

    def __str__(self):
        return """ProjectsCollection(total_count={}, repos={})""".format(
            self.totalCount, self.repos
        )
