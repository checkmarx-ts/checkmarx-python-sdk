# encoding: utf-8
from .Application import Application


class ApplicationsCollection(object):
    def __init__(self, total_count, filtered_total_count, applications):
        """

        Args:
            total_count (int):
            filtered_total_count (int):
            applications (`list` of `Application`):
        """
        self.totalCount = total_count
        self.filteredTotalCount = filtered_total_count
        self.applications = applications

    def __str__(self):
        return """ApplicationsCollection(totalCount={totalCount}, filteredTotalCount={filteredTotalCount}, 
        applications={applications})""".format(
            totalCount=self.totalCount, filteredTotalCount=self.filteredTotalCount,
            applications=self.applications
        )
