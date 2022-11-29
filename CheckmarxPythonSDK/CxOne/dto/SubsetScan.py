# encoding: utf-8
class SubsetScan(object):
    def __init__(self, scan_id, created_at, updated_at, status, user_agent, initiator, branch, engines, source_type,
                 source_origin):
        """

        Args:
            scan_id (str): A unique identifier for a scan
            created_at (str):
            updated_at (str):
            status (str):
            user_agent (str): The user-agent header that created the scan
            initiator (str): The user name that created the scan
            branch (str): The scan branch
            engines (list of str): 	The scan engines
            source_type (str): The scan last Source type (e.g. zip, github, gitlab)
            source_origin (str): The scan last origin (e.g. Jenkins, Checkmarx AST, Github action, Github Webhook)
        """
        self.id = scan_id
        self.createdAt = created_at
        self.updatedAt = updated_at
        self.status = status
        self.userAgent = user_agent
        self.initiator = initiator
        self.branch = branch
        self.engines = engines
        self.sourceType = source_type
        self.sourceOrigin = source_origin

    def __str__(self):
        return """SubsetScan(id={}, createdAt={}, updatedAt={}, status={}, userAgent={}, initiator={}, branch={},
        engines={}, sourceType={}，sourceOrigin={})""".format(
            self.id,
            self.createdAt,
            self.updatedAt,
            self.status,
            self.userAgent,
            self.initiator,
            self.branch,
            self.engines,
            self.sourceType,
            self.sourceOrigin,
        )
