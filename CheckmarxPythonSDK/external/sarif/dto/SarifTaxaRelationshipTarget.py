from .SarifToolComponent import SarifToolComponent


class SarifTaxaRelationshipTarget:
    def __init__(self, target_id, index, tool_component):
        """

        Args:
            target_id (str):
            index (int):
            tool_component (SarifToolComponent):
        """
        self.ID = target_id
        self.Index = index
        self.ToolComponent = tool_component

    def __str__(self):
        return f"SarifTaxaRelationshipTarget(" \
               f"target_id={self.ID}, "\
               f"index={self.Index}, "\
               f"tool_component={self.ToolComponent}"\
               f")"
