# encoding: utf-8
class ProjectsCollection(object):
    def __init__(self, total_count, filtered_total_count, projects):
        """

        Args:
            total_count (int): The number of total records
            filtered_total_count (int): The number of total records matching the applied filter
            projects: The projects returned with the filter applied
        """
        self.totalCount = total_count
        self.filteredTotalCount = filtered_total_count
        self.projects = projects

    def __str__(self):
        return """ProjectsCollection(total_count={}, filtered_total_count={}, projects={})""".format(
            self.totalCount, self.filteredTotalCount, self.projects
        )
