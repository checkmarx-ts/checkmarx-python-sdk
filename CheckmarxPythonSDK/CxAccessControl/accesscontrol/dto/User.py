from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    id: Optional[int] = None
    username: Optional[str] = None
    last_login_date: Optional[str] = None
    role_ids: Optional[List[int]] = None
    team_ids: Optional[List[int]] = None
    authentication_provider_id: Optional[int] = None
    creation_date: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    cell_phone_number: Optional[str] = None
    job_title: Optional[str] = None
    other: Optional[str] = None
    country: Optional[str] = None
    active: Optional[bool] = None
    expiration_date: Optional[str] = None
    allowed_ip_list: Optional[List[str]] = None
    locale_id: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "User":
        return cls(
            id=item.get("id"),
            # some endpoints return "userName", others return lowercase "username"
            username=item.get("userName") or item.get("username"),
            last_login_date=item.get("lastLoginDate"),
            role_ids=item.get("roleIds"),
            team_ids=item.get("teamIds"),
            authentication_provider_id=item.get("authenticationProviderId"),
            creation_date=item.get("creationDate"),
            # LDAP/Windows domain user entries use lowercase "firstname"/"lastname"
            first_name=item.get("firstName") or item.get("firstname"),
            last_name=item.get("lastName") or item.get("lastname"),
            email=item.get("email"),
            phone_number=item.get("phoneNumber"),
            cell_phone_number=item.get("cellPhoneNumber"),
            job_title=item.get("jobTitle"),
            other=item.get("other"),
            country=item.get("country"),
            active=item.get("active"),
            expiration_date=item.get("expirationDate"),
            allowed_ip_list=item.get("allowedIpList"),
            locale_id=item.get("localeId"),
        )
