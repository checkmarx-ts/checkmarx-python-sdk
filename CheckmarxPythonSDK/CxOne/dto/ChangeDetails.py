from dataclasses import dataclass


@dataclass
class ChangeDetails:
    """

    Attributes:
        engine_version_changed (booL):
        engine_version_changed_details (str):
        query_changed (bool):
        query_changed_details (str):
        code_change (bool):
        code_change_details (str):
    """

    engine_version_changed: bool = None
    engine_version_changed_details: str = None
    query_changed: bool = None
    query_changed_details: str = None
    code_change: bool = None
    code_change_details: str = None
    
    
def construct_change_details(item):
    return ChangeDetails(
            engine_version_changed=item.get("engineVersionChanged"),
            engine_version_changed_details=item.get("engineVersionChangeDetails"),
            query_changed=item.get("queryChanged"),
            query_changed_details=item.get("queryChangeDetails"),
            code_change=item.get("codeChanged"),
            code_change_details=item.get("codeChangeDetails")
        )
