# encoding: utf-8
import json
from .httpRequests import get_request, put_request, get_headers
from CheckmarxPythonSDK.utilities.compat import OK
from .sast.configuration.dto import CxSASTConfig
from .sast.general.dto import CxServerLicenseData, CxSupportedLanguage

class GeneralAPI:
    """
    CxSAST general API
    """
    @staticmethod
    def get_server_license_data(api_version="4.0"):
        """
        Returns the CxSAST server's license data
        """
        result = None
        relative_url = "/cxrestapi/serverLicenseData"
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            json = response.json()
            result = CxServerLicenseData(
                current_audit_users = json["currentAuditUsers"],
                current_projects_count = json["currentProjectsCount"],
                current_users = json["currentUsers"],
                edition = json["edition"],
                expiration_date = json["expirationDate"],
                hid = json["hid"],
                is_osa_enabled = json["isOsaEnabled"],
                max_audit_users = json["maxAuditUsers"],
                max_concurrent_scans = json["maxConcurrentScans"],
                max_loc = json["maxLOC"],
                max_users = json["maxUsers"],
                osa_expiration_date = json["osaExpirationDate"],
                projects_allowed = json["projectsAllowed"],
                supported_languages = [
                    CxSupportedLanguage(
                        is_supported = item["isSupported"],
                        language = item["language"])
                    for item in json["supportedLanguages"]
                    ]
                )
        return result
