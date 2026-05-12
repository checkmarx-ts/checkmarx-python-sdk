from dataclasses import dataclass


@dataclass
class MemoryInfoRepresentation:
    free: ... = None
    free_formated: ... = None
    free_percentage: ... = None
    total: ... = None
    total_formated: ... = None
    used: ... = None
    used_formated: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "MemoryInfoRepresentation":
        return cls(
            free=item.get("free"),
            free_formated=item.get("freeFormated"),
            free_percentage=item.get("freePercentage"),
            total=item.get("total"),
            total_formated=item.get("totalFormated"),
            used=item.get("used"),
            used_formated=item.get("usedFormated"),
        )
