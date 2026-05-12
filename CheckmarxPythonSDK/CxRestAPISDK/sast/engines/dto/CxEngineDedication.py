from dataclasses import dataclass
from typing import Optional


@dataclass
class CxEngineDedication:

    item_type: Optional[str] = None
    item_id: Optional[str] = None
    item_name: Optional[str] = None
    is_deprecated: Optional[bool] = None

    def __post_init__(self):
        if self.item_type and self.item_type not in ["Scan", "Project", "Team"]:
            raise ValueError(
                "parameter item_type should be one of member from list ['Scan', 'Project', 'Team']"
            )

    @classmethod
    def from_dict(cls, item: dict) -> "CxEngineDedication":
        return cls(
            item_type=item.get("itemType"),
            item_id=item.get("itemId"),
            item_name=item.get("itemName"),
            is_deprecated=item.get("isDeprecated"),
        )

    def to_dict(self):
        return {
            "itemType": self.item_type,
            "itemId": self.item_id,
        }
