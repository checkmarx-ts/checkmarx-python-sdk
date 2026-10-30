from dataclasses import dataclass, field
from typing import List, Optional

from .DastApiFileWithType import DastApiFileWithType
from .DastAuthSessionCredentials import DastAuthSessionCredentials
from .DastFileInfo import DastFileInfo
from .DastScanConfig import DastScanConfig


@dataclass
class DastAuthSession:
    """Response from GET /authSession/{envId} and GET /authSession/{envId}/masked.

    Only the fields that are populated depend on `method`
    (NO_AUTH/CREDENTIALS/CONFIG/RECORDING/BROWSER/...); most are None.

    Attributes:
        uuid (Optional[str]): The auth session's UUID.
        method (Optional[str]): Auth method, e.g. NO_AUTH, CREDENTIALS, CONFIG.
        credentials (Optional[DastAuthSessionCredentials]): Set when
            method=CREDENTIALS.
        totp (Optional[dict]): TOTP settings (SecretKey/OTPLength/Period),
            left as a raw dict — never observed populated live, so the
            exact wire shape isn't confirmed.
        file (Optional[DastFileInfo]): The uploaded config/recording file,
            set when method=CONFIG or RECORDING.
        scan_config (Optional[DastScanConfig]): The scanner's resolved
            auth configuration (same shape as DastEnvironment's scanConfig).
        url (Optional[str]): The environment's URL.
        scan_type (Optional[str]): The environment's scan type.
        settings (Optional[dict]): The environment's settings as echoed
            back by the auth session service. Left as a raw dict: the
            live shape includes fields (e.g. authSettings.userName/
            password/verificationMethod/pollFrequency) that aren't in
            the documented EnvSettings/AuthSettings schemas, so a typed
            DTO would either drop live data or assert an unconfirmed shape.
        api_type (Optional[str]): Set when the environment has an API
            definition file. OPENAPI, POSTMAN, HAR, SOAP, or GRAPHQL.
        api_file_type (Optional[str]): Legacy single-file api type field.
        api_url (Optional[str]): Legacy single-file api base URL.
        api_file_name (Optional[str]): Legacy single-file file name.
        api_file (Optional[DastFileInfo]): Legacy single API file.
        api_files (List[DastApiFileWithType]): Current multi-file API
            definitions.
        proxy_recorder_files (List[DastFileInfo]): Uploaded proxy
            recorder files.
        is_public (Optional[bool]): Whether the environment is public.
        browser_id (Optional[str]): Browser used for browser-based auth.
    """
    uuid: Optional[str] = None
    method: Optional[str] = None
    credentials: Optional[DastAuthSessionCredentials] = None
    totp: Optional[dict] = None
    file: Optional[DastFileInfo] = None
    scan_config: Optional[DastScanConfig] = None
    url: Optional[str] = None
    scan_type: Optional[str] = None
    settings: Optional[dict] = None
    api_type: Optional[str] = None
    api_file_type: Optional[str] = None
    api_url: Optional[str] = None
    api_file_name: Optional[str] = None
    api_file: Optional[DastFileInfo] = None
    api_files: List[DastApiFileWithType] = field(default_factory=list)
    proxy_recorder_files: List[DastFileInfo] = field(default_factory=list)
    is_public: Optional[bool] = None
    browser_id: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAuthSession":
        return cls(
            uuid=item.get("uuid"),
            method=item.get("method"),
            credentials=(
                DastAuthSessionCredentials.from_dict(item["Credentials"])
                if item.get("Credentials") else None
            ),
            totp=item.get("TOTP"),
            file=DastFileInfo.from_dict(item["File"]) if item.get("File") else None,
            scan_config=(
                DastScanConfig.from_dict(item["ScanConfig"])
                if item.get("ScanConfig") else None
            ),
            url=item.get("URL"),
            scan_type=item.get("scanType"),
            settings=item.get("Settings"),
            api_type=item.get("apiType"),
            api_file_type=item.get("apiFileType"),
            api_url=item.get("apiURL"),
            api_file_name=item.get("apiFileName"),
            api_file=(
                DastFileInfo.from_dict(item["APIFile"]) if item.get("APIFile") else None
            ),
            api_files=[
                DastApiFileWithType.from_dict(f) for f in (item.get("apiFiles") or [])
            ],
            proxy_recorder_files=[
                DastFileInfo.from_dict(f["File"])
                for f in (item.get("proxyRecorderFiles") or [])
                if f.get("File")
            ],
            is_public=item.get("isPublic"),
            browser_id=item.get("browserId"),
        )
