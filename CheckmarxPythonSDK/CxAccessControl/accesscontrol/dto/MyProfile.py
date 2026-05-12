from dataclasses import dataclass
from typing import Optional


@dataclass
class MyProfile:
    id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    cellphone_number: Optional[str] = None
    job_title: Optional[str] = None
    other: Optional[str] = None
    country: Optional[str] = None
    locale_id: Optional[int] = None
    teams: Optional[list] = None
    authentication_provider_id: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "MyProfile":
        return cls(
            id=item.get("id"),
            username=item.get("userName"),
            first_name=item.get("firstName"),
            last_name=item.get("lastName"),
            email=item.get("email"),
            phone_number=item.get("phoneNumber"),
            cellphone_number=item.get("cellPhoneNumber"),
            job_title=item.get("jobTitle"),
            other=item.get("other"),
            country=item.get("country"),
            locale_id=item.get("localeId"),
            teams=item.get("teams"),
            authentication_provider_id=item.get("authenticationProviderId"),
        )
