# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxScanSettings:
    """
    scan settings
    """

    project: Optional[object] = None
    preset: Optional[object] = None
    engine_configuration: Optional[object] = None
    post_scan_action: Optional[object] = None
    email_notification: Optional[object] = None
    post_scan_action_data: Optional[str] = None
    post_scan_action_name: Optional[str] = None
    post_scan_action_conditions: Optional[object] = None
    post_scan_action_arguments: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanSettings":
        return cls(
            project=item.get("project"),
            preset=item.get("preset"),
            engine_configuration=item.get("engineConfiguration"),
            post_scan_action=item.get("postScanAction"),
            email_notification=item.get("emailNotifications"),
            post_scan_action_data=item.get("postScanActionData"),
            post_scan_action_name=item.get("postScanActionName"),
            post_scan_action_conditions=item.get("postScanActionConditions"),
            post_scan_action_arguments=item.get("postScanActionArguments"),
        )
