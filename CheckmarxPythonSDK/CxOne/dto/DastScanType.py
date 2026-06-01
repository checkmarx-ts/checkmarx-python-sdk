from .StrEnum import StrEnum


class DastScanType(StrEnum):
    """Type of DAST scan to run on an Environment."""
    DAST = "DAST"          # Web
    DAST_API = "DASTAPI"   # API
