from .CxCreateProjectRequest import CxCreateProjectRequest
from .CxCreateProjectResponse import CxCreateProjectResponse
from .CxCredential import CxCredential
from .CxCustomRemoteSourceSettings import CxCustomRemoteSourceSettings
from .CxGitSettings import CxGitSettings
from .CxIssueTrackingSystem import CxIssueTrackingSystem
from .CxIssueTrackingSystemDetail import CxIssueTrackingSystemDetail
from .CxIssueTrackingSystemField import CxIssueTrackingSystemField
from .CxIssueTrackingSystemFieldAllowedValue import CxIssueTrackingSystemFieldAllowedValue
from .CxIssueTrackingSystemJira import CxIssueTrackingSystemJira
from .CxIssueTrackingSystemJiraField import CxIssueTrackingSystemJiraField
from .CxIssueTrackingSystemType import CxIssueTrackingSystemType
from .CxLink import CxLink
from .CxPerforceSettings import CxPerforceSettings
from .CxProject import CxProject
from .CxProjectExcludeSettings import CxProjectExcludeSettings
from .CxSharedRemoteSourceSettingsRequest import CxSharedRemoteSourceSettingsRequest
from .CxSharedRemoteSourceSettingsResponse import CxSharedRemoteSourceSettingsResponse
from .CxSourceSettingsLink import CxSourceSettingsLink
from .CxSVNSettings import CxSVNSettings
from .CxTFSSettings import CxTFSSettings
from .CxUpdateProjectNameTeamIdRequest import CxUpdateProjectNameTeamIdRequest
from .CxUpdateProjectRequest import CxUpdateProjectRequest
from .CxURI import CxURI
from .presets.CxPreset import CxPreset
from .customFields.CxCustomField import CxCustomField
from .customTasks.CxCustomTask import CxCustomTask
from .CxProjectQueueSetting import CxProjectQueueSetting


def construct_cx_project(item):
    """

    Args:
        item (dict):

    Returns:
        `CxProject`
    """
    return CxProject(
        project_id=item.get("id"),
        team_id=item.get("teamId"),
        name=item.get("name"),
        is_public=item.get("isPublic"),
        source_settings_link=CxSourceSettingsLink(
            (item.get("sourceSettingsLink", {}) or {}).get("type"),
            (item.get("sourceSettingsLink", {}) or {}).get("rel"),
            (item.get("sourceSettingsLink", {}) or {}).get("uri")
        ),
        link=CxLink(
            (item.get("link", {}) or {}).get("rel"),
            (item.get("link", {}) or {}).get("uri")
        ),
        custom_fields=[
            CxCustomField(
                custom_field_id=custom_field.get("id"),
                value=custom_field.get("value"),
                name=custom_field.get("name")
            ) for custom_field in item.get("customFields")
        ],
        links=[
            CxLink(
                rel=link.get("rel"),
                uri=link.get("uri"),
            ) for link in item.get("links")
        ],
        project_queue_settings=CxProjectQueueSetting(
            queue_keep_mode=item.get("projectQueueSettings", {}).get("queueKeepMode"),
            scans_type=item.get("projectQueueSettings", {}).get("scansType"),
            include_scans_in_process=item.get("projectQueueSettings", {}).get("includeScansInProcess"),
            identical_code_only=item.get("projectQueueSettings", {}).get("identicalCodeOnly"),
        ),
    )

