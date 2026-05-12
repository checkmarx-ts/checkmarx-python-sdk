# encoding: utf-8
import datetime
import logging
from dataclasses import dataclass
from typing import List, Optional
from .CxSupportedLanguage import CxSupportedLanguage

logger = logging.getLogger("CheckmarxPythonSDK")


def parse_expiration_date(date_str):
    """
    Parse a date string in MM/DD/YYYY format into a datetime.date object. If
    the string cannot be parsed, we return it instead.
    """
    bits = date_str.split("/")
    try:
        return datetime.date(int(bits[2]), int(bits[0]), int(bits[1]))
    except:
        logger.debug("Cannot parse {} as MM/DD/YYYY".format(date_str))
        return date_str


@dataclass
class CxServerLicenseData:
    """
    CxSAST server license data
    """

    current_audit_users: Optional[int] = None
    current_projects_count: Optional[int] = None
    current_users: Optional[int] = None
    edition: Optional[str] = None
    expiration_date: Optional[object] = None
    hid: Optional[str] = None
    is_osa_enabled: Optional[bool] = None
    max_audit_users: Optional[int] = None
    max_concurrent_scans: Optional[int] = None
    max_loc: Optional[int] = None
    max_users: Optional[int] = None
    osa_expiration_date: Optional[object] = None
    projects_allowed: Optional[int] = None
    supported_languages: Optional[List[CxSupportedLanguage]] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxServerLicenseData":
        osa_exp = item.get("osaExpirationDate")
        return cls(
            current_audit_users=item.get("currentAuditUsers"),
            current_projects_count=item.get("currentProjectsCount"),
            current_users=item.get("currentUsers"),
            edition=item.get("edition"),
            expiration_date=parse_expiration_date(item.get("expirationDate", "")),
            hid=item.get("hid"),
            is_osa_enabled=item.get("isOsaEnabled"),
            max_audit_users=item.get("maxAuditUsers"),
            max_concurrent_scans=item.get("maxConcurrentScans"),
            max_loc=item.get("maxLOC"),
            max_users=item.get("maxUsers"),
            osa_expiration_date=(
                None if not osa_exp else parse_expiration_date(osa_exp)
            ),
            projects_allowed=item.get("projectsAllowed"),
            supported_languages=[
                CxSupportedLanguage.from_dict(s)
                for s in (item.get("supportedLanguages") or [])
            ],
        )
