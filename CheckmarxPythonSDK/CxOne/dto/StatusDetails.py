from dataclasses import dataclass


@dataclass
class StatusDetails:
    name: str
    status: str
    details: str
    start_date: str
    end_date: str
    loc: int | None = None # Only for SAST

    def to_dict(self):
        data = {
            "name": self.name,
            "status": self.status,
            "details": self.details,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
        if self.loc:
            data["loc"] = self.loc
        return data

    def __repr__(self):
        loc = f", loc={self.loc}" if self.loc else ""
        return f"StatusDetails(" \
            f"name='{self.name}', " \
            f"status='{self.status}', " \
            f"details='{self.details}', " \
            f"start_date='{self.start_date}', " \
            f"end_date='{self.end_date}'" \
            f"{loc}" \
            f")"

def construct_status_details(item):
    return StatusDetails(
        name=item.get("name"),
        status=item.get("status"),
        details=item.get("details"),
        loc=item.get("loc"),
        start_date=item.get("startDate"),
        end_date=item.get("endDate")
    )
