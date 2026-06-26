from dataclasses import dataclass, asdict


@dataclass
class PackageActionValue:
    """The value associated with a package action.

    Attributes:
        state (str): The state to apply. 'Muted' ignores the package
            indefinitely; 'Snooze' ignores until endDate; 'Monitored'
            restores normal monitoring.
        endDate (str): ISO-8601 timestamp marking the end of the snooze
            period. Required when state is 'Snooze'.
    """

    state: str
    endDate: str = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
