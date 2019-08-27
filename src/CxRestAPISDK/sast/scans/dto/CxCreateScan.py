# encoding: utf-8

import json


class CxCreateScan(object):
    """
    the data when create scan
    """

    def __init__(self, project_id, is_incremental, is_public, force_scan, comment):
        """

        Args:
            project_id (int):
            is_incremental (bool):
            is_public (bool):
            force_scan (bool):
            comment (str):
        """
        self.project_id = project_id
        self.is_incremental = is_incremental
        self.is_public = is_public
        self.force_scan = force_scan
        self.comment = comment

    def get_post_data(self):
        return json.dumps(
            {
                "projectId": self.project_id,
                "isIncremental": self.is_incremental,
                "isPublic": self.is_public,
                "forceScan": self.force_scan,
                "comment": self.comment
            }
        )

    def __str__(self):
        return "CxCreateScan(project_id={}, is_incremental={}, is_public={}, force_scan={}, comment={})".format(
            self.project_id, self.is_incremental, self.is_public, self.force_scan, self.comment
        )
