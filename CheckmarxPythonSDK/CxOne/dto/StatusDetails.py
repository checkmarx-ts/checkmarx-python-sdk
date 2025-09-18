from dataclasses import dataclass


@dataclass
class StatusDetails:
    name: str
    status: str
    details: str
    start_date: str
    end_date: str

    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "details": self.details,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }


def construct_status_details(item):
    return StatusDetails(
        name=item.get("name"),
        status=item.get("status"),
        details=item.get("details"),
        start_date=item.get("startDate"),
        end_date=item.get("endDate")
    )
