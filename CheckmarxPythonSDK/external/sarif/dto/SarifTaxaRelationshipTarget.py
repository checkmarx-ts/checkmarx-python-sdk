from .SarifToolComponent import SarifToolComponent


class SarifTaxaRelationshipTarget:
    def __init__(self, target_id, index, tool_component):
        """

        Args:
            target_id (str):
            index (int):
            tool_component (SarifToolComponent):
        """
        self.id = target_id
        self.index = index
        self.toolComponent = tool_component

    def __str__(self):
        return f"SarifTaxaRelationshipTarget(" \
               f"target_id={self.id}, "\
               f"index={self.index}, "\
               f"tool_component={self.toolComponent}"\
               f")"
