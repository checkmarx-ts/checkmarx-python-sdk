# encoding: utf-8
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CxProject:
    """
    the project details
    """

    project_id: Optional[int] = None
    team_id: Optional[str] = None
    name: Optional[str] = None
    is_public: Optional[bool] = None
    source_settings_link: Optional[object] = None
    custom_fields: Optional[List] = None
    links: Optional[List] = None
    project_queue_settings: Optional[object] = None
    owner: Optional[str] = None
    is_deprecated: Optional[bool] = None
    is_branched: Optional[bool] = None
    original_project_id: Optional[int] = None
    branched_on_scan_id: Optional[int] = None
    related_projects: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxProject":
        from .CxSourceSettingsLink import CxSourceSettingsLink
        from .customFields.CxCustomField import CxCustomField
        from .CxLink import CxLink
        from .CxProjectQueueSetting import CxProjectQueueSetting

        ssl = item.get("sourceSettingsLink") or {}
        return cls(
            project_id=item.get("id"),
            team_id=item.get("teamId"),
            name=item.get("name"),
            is_public=item.get("isPublic"),
            source_settings_link=CxSourceSettingsLink(
                source_settings_link_type=ssl.get("type"),
                rel=ssl.get("rel"),
                uri=ssl.get("uri"),
            ),
            custom_fields=[
                CxCustomField.from_dict(cf) for cf in (item.get("customFields") or [])
            ],
            links=[CxLink.from_dict(lnk) for lnk in (item.get("links") or [])],
            owner=item.get("owner"),
            is_deprecated=item.get("isDeprecated"),
            project_queue_settings=CxProjectQueueSetting.from_dict(
                item.get("projectQueueSettings") or {}
            ),
            is_branched=item.get("isBranched"),
            original_project_id=item.get("originalProjectId"),
            branched_on_scan_id=item.get("branchedOnScanId"),
            related_projects=item.get("relatedProjects"),
        )
