from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class FusionResultsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/correlation/results"
        )

    def get_applications(self) -> dict:
        """
        Get a list of scanned application IDs.

        Returns:
            dict with 'applications' list of UUID strings
        """
        url = f"{self.base_url}/applications"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_application_summary(
        self,
        id: str,
        action: List[str] = None,
        access: List[str] = None,
        category: List[str] = None,
        language: List[str] = None,
        type: List[str] = None,
    ) -> dict:
        """
        Get summary of microservices and cloud resources for an application.

        Args:
            id (str): Application ID (uuid)
            action (List[str]): Filter by action (max 3)
            access (List[str]): Filter by access (max 3)
            category (List[str]): Filter by category (max 20)
            language (List[str]): Filter by language (max 50)
            type (List[str]): Filter by resource type (max 50)

        Returns:
            dict with microservices and cloudResources metadata
        """
        url = f"{self.base_url}/applications/{id}/summary"
        params = {
            "action": action,
            "access": access,
            "category": category,
            "language": language,
            "type": type,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_application_resources(
        self,
        id: str,
        access: List[str] = None,
        category: List[str] = None,
        type: List[str] = None,
    ) -> dict:
        """
        Get cloud resources for an application with project IDs.

        Args:
            id (str): Application ID (uuid)
            access (List[str]): Filter by access (max 3)
            category (List[str]): Filter by category (max 20)
            type (List[str]): Filter by resource type (max 50)

        Returns:
            dict with appId, scanId, scanTime, resources
        """
        url = f"{self.base_url}/applications/{id}/resources"
        params = {"access": access, "category": category, "type": type}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_application_microservices(
        self,
        id: str,
        action: List[str] = None,
        language: List[str] = None,
    ) -> dict:
        """
        Get microservices for an application with resources in use.

        Args:
            id (str): Application ID (uuid)
            action (List[str]): Filter by action (max 3)
            language (List[str]): Filter by language (max 50)

        Returns:
            dict with appId, scanId, scanTime, microservices
        """
        url = f"{self.base_url}/applications/{id}/microservices"
        params = {"action": action, "language": language}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_application_risk_scores(
        self, id: str, cxone_scan_ids: List[str] = None
    ) -> dict:
        """
        Get risk score results for an application.

        Args:
            id (str): Application ID (uuid)
            cxone_scan_ids (List[str]): List of scan IDs (max 50)

        Returns:
            dict with totalCount and results
        """
        url = f"{self.base_url}/applications/{id}/risk-scores"
        params = {"cxone-scan-ids": cxone_scan_ids}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()


# ---- Module-level convenience functions ----

def get_applications() -> dict:
    return FusionResultsAPI().get_applications()


def get_application_summary(
    id: str,
    action: List[str] = None,
    access: List[str] = None,
    category: List[str] = None,
    language: List[str] = None,
    type: List[str] = None,
) -> dict:
    return FusionResultsAPI().get_application_summary(
        id=id, action=action, access=access, category=category,
        language=language, type=type,
    )


def get_application_resources(
    id: str,
    access: List[str] = None,
    category: List[str] = None,
    type: List[str] = None,
) -> dict:
    return FusionResultsAPI().get_application_resources(
        id=id, access=access, category=category, type=type,
    )


def get_application_microservices(
    id: str,
    action: List[str] = None,
    language: List[str] = None,
) -> dict:
    return FusionResultsAPI().get_application_microservices(
        id=id, action=action, language=language,
    )


def get_application_risk_scores(
    id: str, cxone_scan_ids: List[str] = None
) -> dict:
    return FusionResultsAPI().get_application_risk_scores(
        id=id, cxone_scan_ids=cxone_scan_ids,
    )
