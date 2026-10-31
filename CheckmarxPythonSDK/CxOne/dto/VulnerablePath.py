from dataclasses import dataclass
from typing import Optional


@dataclass
class VulnerablePath:
    """An entry in VulnerabilityDetail.vulnerable_paths."""
    file_name: Optional[str] = None
    class_: Optional[str] = None
    function_modifier: Optional[str] = None
    function_name: Optional[str] = None
    function_params: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "VulnerablePath":
        return cls(
            file_name=item.get("fileName"),
            class_=item.get("class"),
            function_modifier=item.get("functionModifier"),
            function_name=item.get("functionName"),
            function_params=item.get("functionParams"),
        )
