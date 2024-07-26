class ProjectResponseModel(object):

    def __init__(self, project_id=None, project_name=None, source_origin=None, last_scan_date=None, source_type=None,
                 tags=None, groups_ids=None, risk_level=None, repo_id=None, scm_repo_id=None, total_counters=None,
                 engines_data=None):
        """

        Args:
            project_id (str): The ID of the project.
            project_name (str): The name of the project.
            source_origin (str): The origin of the project source.
            last_scan_date (str): The date of the last scan.
            source_type (str): The type of project source.
            tags (dict): 	A map of project tags.
            groups_ids (list of str): An array of group IDs associated with the project.
            risk_level (str): The overall risk level of the project.
            repo_id (int): The ID of the repository associated with the project.
            scm_repo_id (str): The ID of the SCM repository associated with the project.
            total_counters (TotalCounters):
            engines_data (list of EngineData):
        """
        self.project_id = project_id
        self.project_name = project_name
        self.source_origin = source_origin
        self.last_scan_date = last_scan_date
        self.source_type = source_type
        self.tags = tags
        self.groups_ids = groups_ids
        self.risk_level = risk_level
        self.repo_id = repo_id
        self.scm_repo_id = scm_repo_id
        self.total_counters = total_counters
        self.engines_data = engines_data

    def __str__(self):
        return """ProjectResponseModel(project_id={}, project_name={}, source_origin={}, last_scan_date={}, 
        source_type={}, tags={}, groups_ids={}, risk_level={}, repo_id={}, scm_repo_id={}, total_counters={},
        engines_data={})""".format(
            self.project_id, self.project_name, self.source_origin, self.last_scan_date,
            self.source_type, self.tags, self.groups_ids, self.risk_level, self.repo_id, self.scm_repo_id,
            self.total_counters, self.engines_data
        )
