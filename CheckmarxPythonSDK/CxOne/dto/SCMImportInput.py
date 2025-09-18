from dataclasses import dataclass
from .Scm import Scm
from .ScmOrganization import ScmOrganization
from .ProjectSettings import ProjectSettings
from .ScmProject import ScmProject
from typing import List


@dataclass
class SCMImportInput:
    """

    Attributes:
        scm (Scm):
        organization (ScmOrganization):
        default_project_settings (ProjectSettings): By default, these settings will be applied to each
            project created by this process. You can configure different settings for specific projects, which will
            override these settings.
        scan_projects_after_import (bool): If true an initial scan will be run when the import process is completed
        projects (list of ScmProject): Specify the repos that you would like to import.
            Each repo needs to be submitted explicitly.
            Note: You can specify project settings for each specific project. These settings override the
            defaultProjectSettings
    """

    scm: Scm
    organization: ScmOrganization
    default_project_settings: ProjectSettings
    scan_projects_after_import: bool
    projects: List[ScmProject]

    def to_dict(self):
        return {
            "scm": self.scm.to_dict(),
            "organization": self.organization.to_dict(),
            "defaultProjectSettings": self.default_project_settings.to_dict(),
            "scanProjectsAfterImport": self.scan_projects_after_import,
            "projects": [
                project.to_dict() for project in self.projects or []
            ]
        }
