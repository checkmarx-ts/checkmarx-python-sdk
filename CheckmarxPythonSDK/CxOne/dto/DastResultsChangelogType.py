from .StrEnum import StrEnum


class DastResultsChangelogType(StrEnum):
    """Update scope for POST /changelog.

    - INSTANCE: use the similarityID2 array to target specific result
      instances.
    - ALERT: use alert_similarity_id to update every instance of an
      alert.
    """
    ALERT = "alert"
    INSTANCE = "instance"
