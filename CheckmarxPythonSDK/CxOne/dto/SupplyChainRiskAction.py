from dataclasses import dataclass, field, asdict
from typing import Union


@dataclass
class SupplyChainRiskAction:
    """An action to perform on a supply chain risk.

    Attributes:
        actionType (str): Type of action. 'ChangeState' to update the risk
            state, or 'ChangeScore' to update the risk score.
        value (Union[str, int]): For ChangeState, one of: ToVerify,
            NotExploitable, ProposedNotExploitable, Confirmed, Urgent.
            For ChangeScore, an integer risk score.
        comment (str): A comment explaining the rationale for this action.
    """

    actionType: str
    value: Union[str, int]
    comment: str

    def to_dict(self):
        return {
            "actionType": self.actionType,
            "value": self.value,
            "comment": self.comment,
        }
