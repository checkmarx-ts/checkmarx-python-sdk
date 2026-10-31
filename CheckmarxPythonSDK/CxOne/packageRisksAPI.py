from dataclasses import asdict
from typing import List

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import PackageRisk, PackageRiskItem


class PackageRisksAPI(object):
    """API client for the SCA Data Hub service.

    Note: this service is hosted on its own domain (configured as
    `datahub_base_url`, default https://us.datahub.sca.checkmarx.net),
    separate from the main CxOne host -- but auth is shared, so this
    reuses the same ApiClient/token as the rest of CxOne.
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.datahub_base_url}/api/v1"
        )

    def get_package_risks(
        self,
        items: List[PackageRiskItem],
        format_: str = "Package",
        include_risk_details: bool = None,
        include_version_details: bool = None,
        include_version_remediation: bool = None,
        correlation_id: str = None,
    ) -> List[PackageRisk]:
        """POST /api/v1/Packages/risks -- retrieve vulnerability and
        malware risk data for one or more software packages.

        Packages can be identified either by pURL or by type/name/version
        (set accordingly on each PackageRiskItem, matching `format_`).
        Maximum 100 items per request (server-enforced).

        Args:
            items (List[PackageRiskItem]): Package versions to look up.
            format_ (str): "Package" (default) or "Purl" -- determines
                whether `items` are identified by type/name/version or
                by `purl`.
            include_risk_details (bool): Include risk details.
            include_version_details (bool): Include version details.
            include_version_remediation (bool): Include remediation
                suggestions.
            correlation_id (str): Optional UUID, for internal Checkmarx
                use.

        Returns:
            List[PackageRisk]
        """
        params = {
            "IncludeRiskDetails": include_risk_details,
            "IncludeVersionDetails": include_version_details,
            "IncludeVersionRemediation": include_version_remediation,
        }
        headers = {"Accept": "*/*; version=1.0"}
        if correlation_id:
            headers["CorrelationId"] = correlation_id
        body = {
            "format": format_,
            "items": [asdict(package_item) for package_item in items],
        }
        response = self.api_client.call_api(
            method="POST",
            url=f"{self.base_url}/Packages/risks",
            params=params,
            json=body,
            headers=headers,
        )
        return [PackageRisk.from_dict(risk) for risk in response.json()]


def get_package_risks(
    items: List[PackageRiskItem],
    format_: str = "Package",
    include_risk_details: bool = None,
    include_version_details: bool = None,
    include_version_remediation: bool = None,
    correlation_id: str = None,
) -> List[PackageRisk]:
    return PackageRisksAPI().get_package_risks(
        items=items,
        format_=format_,
        include_risk_details=include_risk_details,
        include_version_details=include_version_details,
        include_version_remediation=include_version_remediation,
        correlation_id=correlation_id,
    )
