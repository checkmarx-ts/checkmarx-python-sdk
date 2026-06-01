from dataclasses import dataclass


@dataclass
class DastResultChangelogEntry:
    """One entry in DastResultDetail.changelog_data."""
    note_text: str = None
    severity: str = None
    state: str = None
    created_by: str = None
    created_at: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastResultChangelogEntry":
        return cls(
            note_text=item.get("note_text"),
            severity=item.get("severity"),
            state=item.get("state"),
            created_by=item.get("created_by"),
            created_at=item.get("created_at"),
        )
