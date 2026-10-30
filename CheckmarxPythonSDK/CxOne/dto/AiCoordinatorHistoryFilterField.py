from .StrEnum import StrEnum


class AiCoordinatorHistoryFilterField(StrEnum):
    """Valid `field` values for GET /history/fieldValues. v1 supports only
    projectNames."""
    PROJECT_NAMES = "projectNames"
