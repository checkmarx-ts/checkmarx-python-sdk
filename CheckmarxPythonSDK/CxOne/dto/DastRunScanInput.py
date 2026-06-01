from dataclasses import dataclass
from typing import List, Union
from .DastScanType import DastScanType


@dataclass
class DastRunScanInput:
    """Request shape for POST /api/dast/scans/scan (multipart form upload).

    Required by the API: environment_id, scan_type, configuration_file.
    File-path fields hold a local path to the file; DastScanAPI.run_scan
    opens them and attaches as multipart parts on send.
    """
    environment_id: str = None
    scan_type: Union[DastScanType, str] = None
    configuration_file: str = None  # local path to the ZAP config file
    api_file: str = None             # local path to an OpenAPI/Swagger file (optional)
    groups: List[str] = None
    tags: List[str] = None
    use_external_worker: bool = None
    use_auth_session: bool = None
    api_file_type: str = None
    cli_version: str = None
    heartbeat_interval: int = None
