from dataclasses import dataclass
from typing import List


@dataclass
class SubsetScan:
    """

    Args:
        id (str): A unique identifier for a scan
        created_at (str):
        updated_at (str):
        status (str):
        user_agent (str): The user-agent header that created the scan
        initiator (str): The username that created the scan
        branch (str): The scan branch
        engines (list of str): 	The scan engines
        source_type (str): The scan last Source type (e.g. zip, github, gitlab)
        source_origin (str): The scan last origin (e.g. Jenkins, Checkmarx AST, Github action, Github Webhook)
    """
    id: str
    created_at: str
    updated_at: str
    status: str
    user_agent: str
    initiator: str
    branch: str
    engines: List[str]
    source_type: str
    source_origin: str


def construct_subset_scan(item):
    return SubsetScan(
        id=item.get("id"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt"),
        status=item.get("status"),
        user_agent=item.get("userAgent"),
        initiator=item.get("initiator"),
        branch=item.get("branch"),
        engines=item.get("engines"),
        source_type=item.get("sourceType"),
        source_origin=item.get("sourceOrigin")
    )
