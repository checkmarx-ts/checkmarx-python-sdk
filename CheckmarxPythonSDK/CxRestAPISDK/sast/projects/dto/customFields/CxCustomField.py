# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxCustomField:
    """
    custom fields
    """

    id: Optional[int] = None
    name: Optional[str] = None
    value: Optional[str] = None
    is_mandatory: Optional[bool] = None
    project_id: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxCustomField":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            value=item.get("value"),
            is_mandatory=item.get("isMandatory"),
            project_id=item.get("projectId"),
        )

    def to_dict(self):
        return {"id": self.id, "value": self.value}
