# encoding: utf-8
import json
from .Git import Git
from .Upload import Upload
from .Project import Project
from .ScanConfig import ScanConfig
from ..utilities import (type_check, list_member_type_check)


class ScanInput(object):

    def __init__(self, scan_type, handler, project=None, configs=(), tags=None):
        """

        Args:
            scan_type (str): The type of the scan.
            handler (`Git`, `Upload`): A JSON object containing info about the 'handler' of the scan submission.
            project (`Project`, optional): A JSON object representing the project to scan
            configs (`List` of `ScanConfig`):
            tags (dict): A JSON object containing a list of the tags associated with the scan, in key-value format.
        """

        if scan_type not in ("upload", "git"):
            raise ValueError("Error for parameter scan_type, can only be 'upload', 'git'. ")
        type_check(handler, (Git, Upload))
        type_check(project, Project)
        type_check(configs, (list, tuple))
        list_member_type_check(configs, ScanConfig)
        type_check(tags, dict)

        self.type = scan_type
        self.handler = handler
        self.project = project
        self.config = configs
        self.tags = tags

    def __str__(self):
        return """ScanInput(type={}, handler={}, project={}, config={}, tags={})""".format(
            self.type, self.handler, self.project, self.config, self.tags
        )

    def get_post_data(self):
        return json.dumps({
            "type": self.type,
            "handler": self.handler.as_dict(),
            "project": self.project.as_dict() if self.project else self.project,
            "config": [config.as_dict() for config in self.config or []],
            "tags": self.tags
        })
