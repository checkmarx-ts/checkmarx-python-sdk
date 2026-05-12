from dataclasses import dataclass
from typing import Optional


@dataclass
class SAMLIdentityProvider:
    id: Optional[int] = None
    certificate_file_name: Optional[str] = None
    certificate_subject: Optional[str] = None
    active: Optional[bool] = None
    name: Optional[str] = None
    issuer: Optional[str] = None
    login_url: Optional[str] = None
    logout_url: Optional[str] = None
    error_url: Optional[str] = None
    sign_authn_request: Optional[bool] = None
    authn_request_binding: Optional[str] = None
    is_manual_management: Optional[bool] = None
    default_team_id: Optional[int] = None
    default_role_id: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "SAMLIdentityProvider":
        return cls(
            id=item.get("id"),
            certificate_file_name=item.get("certificateFileName"),
            certificate_subject=item.get("certificateSubject"),
            active=item.get("active"),
            name=item.get("name"),
            issuer=item.get("issuer"),
            login_url=item.get("loginUrl"),
            logout_url=item.get("logoutUrl"),
            error_url=item.get("errorUrl"),
            sign_authn_request=item.get("signAuthnRequest"),
            authn_request_binding=item.get("authnRequestBinding"),
            is_manual_management=item.get("isManualManagement"),
            default_team_id=item.get("defaultTeamId"),
            default_role_id=item.get("defaultRoleId"),
        )
