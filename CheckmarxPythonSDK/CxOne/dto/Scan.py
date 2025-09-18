from typing import List
from .StatusDetails import StatusDetails, construct_status_details
from dataclasses import dataclass


@dataclass
class Scan:
    """

    Args:
        id (str): The unique identifier of the scan.
        status (str): The execution status of the scan.
                Enum:[ Queued, Running, Completed, Failed, Partial, Canceled ]
        status_details (`list` of `StatusDetails`):
        position_in_queue (int): the position of the scan in the execution queue.
        project_id (str): The associated project id
        project_name (str):
        branch (str): The git branch
        commit_id (str): The git commit id. Mutually exclusive to commitTag
        commit_tag (str): The git tag. Mutually exclusive to commitId
        upload_url (str): The URL pointing to the location of the uploaded file that was scanned.
        created_at (str): The date and time that the scan was created.
        updated_at (str): The date and time that the scan was created.
        user_agent (str): The user-agent header of the tool/platform that initiated the scan
        initiator (str): An identifier of the user who created the scan.
        tags (dict): An object representing the scan tags in a key-value format
        metadata (dict): A JSON object containing info about the scan settings.
    """

    id: str
    status: str
    status_details: List[StatusDetails]
    position_in_queue: int
    project_id: str
    project_name: str
    branch: str
    commit_id: str
    commit_tag: str
    upload_url: str
    created_at: str
    updated_at: str
    user_agent: str
    initiator: str
    tags: dict
    metadata: dict
    engines: List[str] = None
    source_type: str = None
    source_origin: str = None


def construct_scan(item):
    return Scan(
        id=item.get("id"),
        status=item.get("status"),
        status_details=[
            construct_status_details(detail) for detail in item.get("statusDetails", [])
        ],
        position_in_queue=item.get("positionInQueue"),
        project_id=item.get("projectId"),
        project_name=item.get("projectName"),
        branch=item.get("branch"),
        commit_id=item.get("commitId"),
        commit_tag=item.get("commitTag"),
        upload_url=item.get("uploadUrl"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt"),
        user_agent=item.get("userAgent"),
        initiator=item.get("initiator"),
        tags=item.get("tags"),
        metadata=item.get("metadata"),
        engines=item.get("engines"),
        source_type=item.get("sourceType"),
        source_origin=item.get("sourceOrigin")
    )
