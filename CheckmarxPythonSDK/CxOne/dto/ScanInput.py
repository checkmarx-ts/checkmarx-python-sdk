from dataclasses import dataclass
from typing import List, Union
from .Git import Git
from .Upload import Upload
from .Project import Project
from .ScanConfig import ScanConfig


@dataclass
class ScanInput:
    """

    Args:
        type (str): The type of the scan.
        handler (`Git`, `Upload`): A JSON object containing info about the 'handler' of the scan submission.
        project (`Project`, optional): A JSON object representing the project to scan
        configs (`List` of `ScanConfig`):
        tags (dict): A JSON object containing a list of the tags associated with the scan, in key-value format.
    """
    type: str
    handler: Union[Git, Upload]
    project: Project = None
    configs: List[ScanConfig] = None
    tags: dict = None

    def to_dict(self):
        return {
            "type": self.type,
            "handler": self.handler.to_dict(),
            "project": self.project.to_dict() if self.project else self.project,
            "config": [
                config.to_dict() for config in self.configs or []
            ],
            "tags": self.tags
        }
