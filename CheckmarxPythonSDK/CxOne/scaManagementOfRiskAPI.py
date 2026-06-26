from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List

from .dto import (
    UpdatePackageStateBulkRequest,
    UpdatePackageStateRequest,
    UpdateSupplyChainRiskRequest,
    UpdateSupplyChainRisksBulkRequest,
)


class ScaManagementOfRiskAPI(object):
    """API client for the SCA Scanner - Management of Risk REST API.

    Enables muting packages and managing the state and risk score of
    vulnerabilities and supply chain risks detected by SCA scans.

    Base URL: {server}/api/sca/management-of-risk
    """

    _base_path = "/api/sca/management-of-risk"

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = self.api_client.configuration.server_base_url

    # =========================================================================
    # Management of Packages
    # =========================================================================

    def update_package_state(
        self, request: UpdatePackageStateRequest
    ) -> bool:
        """Mute a package so that the associated vulnerabilities will be
        ignored in the scan results.

        Alternatively, you can mark packages as "snooze" in order to ignore
        the results for a limited time period. When you "snooze" a package,
        you need to specify the end time until which it will be snoozed.

        For each action, you must add a comment explaining the rationale.

        Args:
            request (UpdatePackageStateRequest): Package state update payload
                containing packageName, packageVersion, packageManager,
                projectId, and actions.

        Returns:
            bool: True if the update was successful.
        """
        url = f"{self.base_url}{self._base_path}/packages"
        body = request.to_dict()
        body["actions"] = [a.to_dict() for a in request.actions]
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json=body,
            headers={"Content-Type": "application/json-patch+json"},
        )
        return response.status_code == 201

    def update_package_state_bulk(
        self, request: UpdatePackageStateBulkRequest
    ) -> bool:
        """Mute several packages so that the associated vulnerabilities will
        be ignored in the scan results.

        Alternatively, you can mark packages as "snooze" to ignore results
        for a limited time period. The same actions are applied to all
        packages in the packagesProfile list.

        Args:
            request (UpdatePackageStateBulkRequest): Bulk update payload
                containing packagesProfile (list of package entries) and
                actions to apply to all of them.

        Returns:
            bool: True if the bulk update was successful.
        """
        url = f"{self.base_url}{self._base_path}/packages/bulk"
        body = {
            "packagesProfile": [
                p.to_dict() for p in request.packagesProfile
            ],
            "actions": [a.to_dict() for a in request.actions],
        }
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json=body,
            headers={"Content-Type": "application/json-patch+json"},
        )
        return response.status_code == 201

    # =========================================================================
    # Management of Risk — Supply Chain Risks
    # =========================================================================

    def update_supply_chain_risk(
        self, request: UpdateSupplyChainRiskRequest
    ) -> dict:
        """Change the state and risk score for a specific instance of a supply
        chain risk (e.g., Suspected Malware).

        For each action, you must add a comment explaining the rationale.
        You can specify one or more projects for which the change will take
        effect.

        Args:
            request (UpdateSupplyChainRiskRequest): Supply chain risk update
                payload containing packageName, packageVersion, packageManager,
                supplyChainRiskId, projectIds, and actions.

        Returns:
            dict: Response from the API containing the created profile.
        """
        url = f"{self.base_url}{self._base_path}/package-supply-chain-risks"
        body = request.to_dict()
        body["actions"] = [a.to_dict() for a in request.actions]
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json=body,
            headers={
                "Content-Type": "application/json-patch+json",
                "Accept": "text/plain, application/json, text/json",
            },
        )
        if response.content:
            return response.json()
        return {}

    def update_supply_chain_risks_bulk(
        self, request: UpdateSupplyChainRisksBulkRequest
    ) -> dict:
        """Change the state and risk score for several specific instances of
        supply chain risks (e.g., Suspected Malware).

        The same actions are applied to all risks in the
        packageSupplyChainRisks list.

        Args:
            request (UpdateSupplyChainRisksBulkRequest): Bulk update payload
                containing packageSupplyChainRisks (list of risk entries) and
                shared actions.

        Returns:
            dict: Response from the API.
        """
        url = (
            f"{self.base_url}{self._base_path}/package-supply-chain-risks/bulk"
        )
        body = {
            "packageSupplyChainRisks": [
                r.to_dict() for r in request.packageSupplyChainRisks
            ],
            "actions": [a.to_dict() for a in request.actions],
        }
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json=body,
            headers={
                "Content-Type": "application/json-patch+json",
                "Accept": "text/plain, application/json, text/json",
            },
        )
        if response.content:
            return response.json()
        return {}

    # =========================================================================
    # Management of Risk — Vulnerabilities
    # =========================================================================

    def update_vulnerability(
        self, vulnerability_data: dict
    ) -> dict:
        """Change the state and risk score for a specific instance of a
        vulnerability.

        Args:
            vulnerability_data (dict): Vulnerability update payload.

        Returns:
            dict: Response from the API.
        """
        url = f"{self.base_url}{self._base_path}/package-vulnerabilities"
        response = self.api_client.call_api(
            method="POST", url=url, json=vulnerability_data
        )
        return response.json()

    def update_vulnerabilities_bulk(
        self, vulnerabilities_data: List[dict]
    ) -> dict:
        """Change the state and risk score for several specific instances of
        vulnerabilities.

        Args:
            vulnerabilities_data (List[dict]): List of vulnerability update
                payloads.

        Returns:
            dict: Response from the API.
        """
        url = (
            f"{self.base_url}{self._base_path}/package-vulnerabilities/bulk"
        )
        response = self.api_client.call_api(
            method="POST", url=url, json=vulnerabilities_data
        )
        return response.json()


# =============================================================================
# Standalone functions
# =============================================================================


def update_package_state(request: UpdatePackageStateRequest) -> bool:
    """Mute a package so that the associated vulnerabilities will be ignored
    in the scan results.

    Alternatively, you can mark packages as "snooze" in order to ignore the
    results for a limited time period. When you "snooze" a package, you need
    to specify the end time until which it will be snoozed.

    For each action, you must add a comment explaining the rationale.

    Args:
        request (UpdatePackageStateRequest): Package state update payload
            containing packageName, packageVersion, packageManager, projectId,
            and actions.

    Returns:
        bool: True if the update was successful.
    """
    return ScaManagementOfRiskAPI().update_package_state(request)


def update_package_state_bulk(
    request: UpdatePackageStateBulkRequest,
) -> bool:
    """Mute several packages so that the associated vulnerabilities will be
    ignored in the scan results.

    Alternatively, you can mark packages as "snooze" to ignore results for a
    limited time period. The same actions are applied to all packages in the
    packagesProfile list.

    Args:
        request (UpdatePackageStateBulkRequest): Bulk update payload containing
            packagesProfile (list of package entries) and actions to apply to
            all of them.

    Returns:
        bool: True if the bulk update was successful.
    """
    return ScaManagementOfRiskAPI().update_package_state_bulk(request)


def update_supply_chain_risk(
    request: UpdateSupplyChainRiskRequest,
) -> dict:
    """Change the state and risk score for a specific instance of a supply
    chain risk (e.g., Suspected Malware).

    For each action, you must add a comment explaining the rationale. You can
    specify one or more projects for which the change will take effect.

    Args:
        request (UpdateSupplyChainRiskRequest): Supply chain risk update payload
            containing packageName, packageVersion, packageManager,
            supplyChainRiskId, projectIds, and actions.

    Returns:
        dict: Response from the API containing the created profile.
    """
    return ScaManagementOfRiskAPI().update_supply_chain_risk(request)


def update_supply_chain_risks_bulk(
    request: UpdateSupplyChainRisksBulkRequest,
) -> dict:
    """Change the state and risk score for several specific instances of supply
    chain risks (e.g., Suspected Malware).

    The same actions are applied to all risks in the packageSupplyChainRisks
    list.

    Args:
        request (UpdateSupplyChainRisksBulkRequest): Bulk update payload
            containing packageSupplyChainRisks (list of risk entries) and
            shared actions.

    Returns:
        dict: Response from the API.
    """
    return ScaManagementOfRiskAPI().update_supply_chain_risks_bulk(request)


def update_vulnerability(vulnerability_data: dict) -> dict:
    """Change the state and risk score for a specific instance of a
    vulnerability.

    Args:
        vulnerability_data (dict): Vulnerability update payload.

    Returns:
        dict: Response from the API.
    """
    return ScaManagementOfRiskAPI().update_vulnerability(vulnerability_data)


def update_vulnerabilities_bulk(vulnerabilities_data: List[dict]) -> dict:
    """Change the state and risk score for several specific instances of
    vulnerabilities.

    Args:
        vulnerabilities_data (List[dict]): List of vulnerability update
            payloads.

    Returns:
        dict: Response from the API.
    """
    return ScaManagementOfRiskAPI().update_vulnerabilities_bulk(
        vulnerabilities_data
    )
