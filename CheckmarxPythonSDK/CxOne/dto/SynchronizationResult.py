from dataclasses import dataclass


@dataclass
class SynchronizationResult:
    added: ... = None
    failed: ... = None
    ignored: ... = None
    removed: ... = None
    status: ... = None
    updated: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "SynchronizationResult":
        return cls(
            added=item.get("added"),
            failed=item.get("failed"),
            ignored=item.get("ignored"),
            removed=item.get("removed"),
            status=item.get("status"),
            updated=item.get("updated"),
        )
