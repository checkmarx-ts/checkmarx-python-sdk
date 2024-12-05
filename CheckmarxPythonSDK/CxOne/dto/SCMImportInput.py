from .Scm import Scm
from .ScmOrganization import ScmOrganization
from .ProjectSettings import ProjectSettings
from .ScmProject import ScmProject
from typing import List


class SCMImportInput(object):

    def __init__(self,
                 scm: Scm,
                 organization: ScmOrganization,
                 default_project_settings: ProjectSettings,
                 scan_projects_after_import: bool,
                 projects: List[ScmProject]
                 ):
        """

        Args:
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
        self.scm = scm
        self.organization = organization
        self.defaultProjectSettings = default_project_settings
        self.scanProjectsAfterImport = scan_projects_after_import
        self.projects = projects

    def __str__(self):
        return (f"SCMImportInput( scm={self.scm}, "
                f"organization={self.organization}, "
                f"defaultProjectSettings={self.defaultProjectSettings}, "
                f"scanProjectsAfterImport={self.scanProjectsAfterImport}, "
                f"projects={self.projects}"
                f")")

    def to_dict(self):
        return {
            "scm": self.scm.to_dict(),
            "organization": self.organization.to_dict(),
            "defaultProjectSettings": self.defaultProjectSettings.to_dict(),
            "scanProjectsAfterImport": self.scanProjectsAfterImport,
            "projects": [project.to_dict() for project in self.projects]
        }
