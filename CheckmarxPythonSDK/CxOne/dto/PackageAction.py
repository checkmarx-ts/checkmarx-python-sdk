from dataclasses import dataclass, asdict

from .PackageActionValue import PackageActionValue


@dataclass
class PackageAction:
    """An action to perform on a package (mute or snooze).

    Attributes:
        actionType (str): Type of action. Currently only 'Ignore' is
            supported, used for muting and snoozing packages.
        value (PackageActionValue): The value for this action, including
            the state ('Ignore' or 'Snooze') and optional endDate.
        comment (str): A comment explaining the rationale for this action.
    """

    actionType: str
    value: PackageActionValue
    comment: str

    def to_dict(self):
        return {
            "actionType": self.actionType,
            "value": self.value.to_dict() if self.value else None,
            "comment": self.comment,
        }
