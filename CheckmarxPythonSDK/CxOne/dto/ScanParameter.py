from dataclasses import dataclass


@dataclass
class ScanParameter:
    key: str = None
    name: str = None
    category: str = None
    originLevel: str = None
    value: str = None
    valueType: str = None
    valueTypeParams: str = None
    allowOverride: bool = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScanParameter":
        return cls(
            key=item.get("key"),
            name=item.get("name"),
            category=item.get("category"),
            originLevel=item.get("originLevel"),
            value=item.get("value"),
            valueType=item.get("valueType"),
            valueTypeParams=item.get("valueTypeParams"),
            allowOverride=item.get("allowOverride"),
        )
