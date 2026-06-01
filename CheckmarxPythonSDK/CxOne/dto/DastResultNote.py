from dataclasses import dataclass


@dataclass
class DastResultNote:
    """One entry in DastResultDetail.notes_data."""
    note_text: str = None
    created_by: str = None
    created_at: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastResultNote":
        return cls(
            note_text=item.get("note_text"),
            created_by=item.get("created_by"),
            created_at=item.get("created_at"),
        )
