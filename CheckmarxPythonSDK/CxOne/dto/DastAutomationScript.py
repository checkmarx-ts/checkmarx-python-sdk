from dataclasses import dataclass
from typing import Union
from .DastAutomationType import DastAutomationType
from .DastAutomationAction import DastAutomationAction
from .DastAutomationScriptType import DastAutomationScriptType
from .DastAutomationEngine import DastAutomationEngine


@dataclass
class DastAutomationScript:
    """settings.automationScripts[] entry on PUT /api/dast/scans/environment.

    All five fields below are required by the API. Pass either enum
    members or raw strings — both serialize correctly.
    """
    type: Union[DastAutomationType, str] = None
    action: Union[DastAutomationAction, str] = None
    script_type: Union[DastAutomationScriptType, str] = None
    inline: str = None
    engine: Union[DastAutomationEngine, str] = None
    name: str = None

    @staticmethod
    def _val(v):
        return v.value if hasattr(v, "value") else v

    def to_dict(self) -> dict:
        raw = {
            "type": self._val(self.type),
            "action": self._val(self.action),
            "scriptType": self._val(self.script_type),
            "inline": self.inline,
            "engine": self._val(self.engine),
            "name": self.name,
        }
        return {k: v for k, v in raw.items() if v is not None}
