from dataclasses import dataclass


@dataclass
class StatusDetails:
    name: str = None
    status: str = None
    details: str = None
    start_date: str = None
    end_date: str = None
    loc: int = None

    def __repr__(self):
        loc = f", loc={self.loc}" if self.loc else ""
        return (
            f"StatusDetails("
            f"name='{self.name}', "
            f"status='{self.status}', "
            f"details='{self.details}', "
            f"start_date='{self.start_date}', "
            f"end_date='{self.end_date}'"
            f"{loc}"
            f")"
        )

    @classmethod
    def from_dict(cls, item: dict) -> "StatusDetails":
        return cls(
            name=item.get("name"),
            status=item.get("status"),
            details=item.get("details"),
            loc=item.get("loc"),
            start_date=item.get("startDate"),
            end_date=item.get("endDate"),
        )
