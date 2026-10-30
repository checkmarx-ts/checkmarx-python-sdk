from typing import List, Optional

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import (
    EnhancedIncidentsPaginationDTO,
    IncidentResultsDTO,
    IncidentsPaginationDto,
    PoliciesPaginationDto,
    PoliciesResultWebDto,
    PolicyShortWebDto,
    PolicyViolationWebDto,
    PolicyWebDto,
    ProjectsInPolicyDto,
    ProjectWebDto,
)


class PolicyManagerAPI(object):
    """API client for the Cx Policy Manager REST API.

    Covers tenant policies (break-build rules evaluated against scan
    results), the incidents and results they generate, and the per-scan
    policy evaluation/violation views.

    Base URL: {server}/api/policy_management_service_uri
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/policy_management_service_uri"
        )

    # =========================================================================
    # Policies
    # =========================================================================

    def get_tenant_policies(self) -> List[PolicyWebDto]:
        """Get all policies for the tenant (unpaginated).

        Returns:
            List[PolicyWebDto]: All tenant policies.
        """
        url = f"{self.base_url}/policies"
        response = self.api_client.call_api(method="GET", url=url)
        return [PolicyWebDto.from_dict(p) for p in response.json()]

    def create_policy(self, policy: PolicyWebDto) -> int:
        """Create a new policy.

        Args:
            policy (PolicyWebDto): The policy to create. `name` is required.

        Returns:
            int: The new policy's ID.
        """
        url = f"{self.base_url}/policies"
        response = self.api_client.call_api(
            method="POST", url=url, json=policy.to_dict()
        )
        return response.json()

    def delete_policies(self, ids: List[int]) -> bool:
        """Delete multiple policies by ID.

        Args:
            ids (List[int]): IDs of the policies to delete.

        Returns:
            bool: True if the request succeeded.
        """
        url = f"{self.base_url}/policies"
        params = {"id": ids}
        response = self.api_client.call_api(
            method="DELETE", url=url, params=params
        )
        return response.status_code in (200, 204)

    def get_policy(self, policy_id: int) -> PolicyWebDto:
        """Get a policy by ID.

        Args:
            policy_id (int): The policy ID.

        Returns:
            PolicyWebDto: The policy.
        """
        url = f"{self.base_url}/policies/{policy_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return PolicyWebDto.from_dict(response.json())

    def update_policy(self, policy_id: int, policy: PolicyWebDto) -> int:
        """Update an existing policy.

        Args:
            policy_id (int): The policy ID.
            policy (PolicyWebDto): The new policy content.

        Returns:
            int: The policy's ID.
        """
        url = f"{self.base_url}/policies/{policy_id}"
        response = self.api_client.call_api(
            method="PUT", url=url, json=policy.to_dict()
        )
        return response.json()

    def delete_policy(self, policy_id: int) -> bool:
        """Delete a policy by ID.

        Args:
            policy_id (int): The policy ID.

        Returns:
            bool: True if the request succeeded.
        """
        url = f"{self.base_url}/policies/{policy_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code in (200, 204)

    def get_policy_v2(self, policy_id: int) -> PolicyWebDto:
        """Get a policy by ID (V2).

        Args:
            policy_id (int): The policy ID.

        Returns:
            PolicyWebDto: The policy.
        """
        url = f"{self.base_url}/policies/v2/{policy_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return PolicyWebDto.from_dict(response.json())

    def update_policy_v2(self, policy_id: int, policy: PolicyWebDto) -> int:
        """Update an existing policy (V2).

        Args:
            policy_id (int): The policy ID.
            policy (PolicyWebDto): The new policy content.

        Returns:
            int: The policy's ID.
        """
        url = f"{self.base_url}/policies/v2/{policy_id}"
        response = self.api_client.call_api(
            method="PUT", url=url, json=policy.to_dict()
        )
        return response.json()

    def get_tenant_policies_with_pagination(
        self, limit: int, page: int, policy_name: str = ""
    ) -> PoliciesPaginationDto:
        """Get tenant policies with pagination.

        Args:
            limit (int): Page size. 1-1000.
            page (int): Page number (1-based).
            policy_name (str): Filter by policy name. Default: "".

        Returns:
            PoliciesPaginationDto: Policies on the page, and the filtered total count.
        """
        url = f"{self.base_url}/policies/v2"
        params = {"limit": limit, "page": page, "policyName": policy_name}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return PoliciesPaginationDto.from_dict(response.json())

    def create_policy_v2(self, policy: PolicyWebDto) -> int:
        """Create a new policy (V2).

        Args:
            policy (PolicyWebDto): The policy to create. `name` is required.

        Returns:
            int: The new policy's ID. (The spec claims this returns a
                PolicyShortWebDto object; live behavior is a bare int,
                same as POST /policies.)
        """
        url = f"{self.base_url}/policies/v2"
        response = self.api_client.call_api(
            method="POST", url=url, json=policy.to_dict()
        )
        return response.json()

    def get_tenant_policies_with_pagination_v3(
        self, limit: int, page: int, policy_name: str = ""
    ) -> PoliciesPaginationDto:
        """Get tenant policies with pagination (V3, path /policies/v3).

        Args:
            limit (int): Page size. 1-1000.
            page (int): Page number (1-based).
            policy_name (str): Filter by policy name. Default: "".

        Returns:
            PoliciesPaginationDto: Policies on the page, and the filtered total count.
        """
        url = f"{self.base_url}/policies/v3"
        params = {"limit": limit, "page": page, "policyName": policy_name}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return PoliciesPaginationDto.from_dict(response.json())

    def get_default_policy(self) -> Optional[PolicyShortWebDto]:
        """Get the tenant's default policy.

        Returns:
            Optional[PolicyShortWebDto]: The default policy's ID and name,
                or None if the tenant has no default policy configured
                (the API responds 200 with an empty body in that case).
        """
        url = f"{self.base_url}/policies/default"
        response = self.api_client.call_api(method="GET", url=url)
        if not response.text:
            return None
        return PolicyShortWebDto.from_dict(response.json())

    def assign_projects_to_policy(
        self, policy_id: int, projects: ProjectsInPolicyDto
    ) -> int:
        """Assign projects to an existing policy.

        Args:
            policy_id (int): The policy ID.
            projects (ProjectsInPolicyDto): Projects to assign.

        Returns:
            int: The policy's ID.
        """
        url = f"{self.base_url}/policies/projects/{policy_id}"
        response = self.api_client.call_api(
            method="PUT", url=url, json=projects.to_dict()
        )
        return response.json()

    def delete_projects_from_policy(
        self, policy_id: int, projects: ProjectsInPolicyDto
    ) -> bool:
        """Remove projects from an existing policy.

        Args:
            policy_id (int): The policy ID.
            projects (ProjectsInPolicyDto): Projects to remove.

        Returns:
            bool: True if the request succeeded.
        """
        url = f"{self.base_url}/policies/projects/{policy_id}"
        response = self.api_client.call_api(
            method="DELETE", url=url, json=projects.to_dict()
        )
        return response.status_code in (200, 204)

    def pin_policy(self, policy_id: int, pin_policy: bool) -> int:
        """Pin or unpin a policy in the policies table.

        Args:
            policy_id (int): The policy ID.
            pin_policy (bool): True to pin, False to unpin.

        Returns:
            int: The policy's ID.
        """
        url = f"{self.base_url}/policies/pinPolicy/{policy_id}/{pin_policy}"
        response = self.api_client.call_api(method="PUT", url=url)
        return response.json()

    # =========================================================================
    # Projects
    # =========================================================================

    def get_tenant_projects(self) -> List[ProjectWebDto]:
        """Get all AST projects known to the Policy Manager service.

        Returns:
            List[ProjectWebDto]: Tenant projects.
        """
        url = f"{self.base_url}/projects"
        response = self.api_client.call_api(method="GET", url=url)
        return [ProjectWebDto.from_dict(p) for p in response.json()]

    def get_projects_tags(self) -> List[str]:
        """Get all AST project tags known to the Policy Manager service.

        Returns:
            List[str]: Project tags.
        """
        url = f"{self.base_url}/projects/tags"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    # =========================================================================
    # Policy violations and evaluation
    # =========================================================================

    def get_policy_violations(
        self, project_id: str, scan_id: str
    ) -> PolicyViolationWebDto:
        """Get policy violations for a project's scan.

        Args:
            project_id (str): The project ID.
            scan_id (str): The scan UUID.

        Returns:
            PolicyViolationWebDto: Policies violated by the scan.
        """
        url = f"{self.base_url}/policy_violations"
        params = {"projectId": project_id, "scanId": scan_id}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return PolicyViolationWebDto.from_dict(response.json())

    def get_evaluated_policies_by_scan_id_and_project_id(
        self, scan_id: str, ast_project_id: str
    ) -> PoliciesResultWebDto:
        """Get the policy evaluation result for a scan and project.

        Args:
            scan_id (str): The scan UUID.
            ast_project_id (str): The project ID.

        Returns:
            PoliciesResultWebDto: Overall status, breakBuild flag, and
                per-policy evaluation results.
        """
        url = f"{self.base_url}/evaluation"
        params = {"scanId": scan_id, "astProjectId": ast_project_id}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return PoliciesResultWebDto.from_dict(response.json())

    # =========================================================================
    # Incidents
    # =========================================================================

    def get_tenant_incidents(self) -> IncidentsPaginationDto:
        """Get all tenant incidents (unpaginated).

        Returns:
            IncidentsPaginationDto: Incidents and the filtered total count.
        """
        url = f"{self.base_url}/incidents"
        response = self.api_client.call_api(method="GET", url=url)
        return IncidentsPaginationDto.from_dict(response.json())

    def get_tenant_incidents_total_count(self) -> int:
        """Get the tenant's total incident count.

        Returns:
            int: Total number of incidents.
        """
        url = f"{self.base_url}/incidents/total"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_tenant_incidents_with_pagination(
        self, limit: int, page: int, incident_name: str = ""
    ) -> IncidentsPaginationDto:
        """Get tenant incidents with pagination.

        Args:
            limit (int): Page size. 1-1000.
            page (int): Page number (1-based).
            incident_name (str): Filter by incident name. Default: "".

        Returns:
            IncidentsPaginationDto: Incidents on the page, and the filtered
                total count.
        """
        url = f"{self.base_url}/incidents/"
        params = {"limit": limit, "page": page, "incidentName": incident_name}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return IncidentsPaginationDto.from_dict(response.json())

    def get_tenant_incidents_with_pagination_and_filters(
        self,
        limit: int,
        page: int,
        policy_name: str = "",
        rule_name: str = "",
        scan_id: str = "",
        project_name: str = "",
        branch: str = "",
        scan_date: str = "",
    ) -> IncidentsPaginationDto:
        """Get tenant incidents with pagination and filters.

        Args:
            limit (int): Page size. 1-1000.
            page (int): Page number (1-based).
            policy_name (str): Filter by policy name. Default: "".
            rule_name (str): Filter by rule name. Default: "".
            scan_id (str): Filter by scan UUID. Default: "".
            project_name (str): Filter by project name. Default: "".
            branch (str): Filter by branch. Default: "".
            scan_date (str): Filter by scan date. Default: "".

        Returns:
            IncidentsPaginationDto: Incidents on the page, and the filtered
                total count.
        """
        url = f"{self.base_url}/incidents/filters"
        params = {
            "limit": limit,
            "page": page,
            "policyName": policy_name,
            "ruleName": rule_name,
            "scanId": scan_id,
            "projectName": project_name,
            "branch": branch,
            "scanDate": scan_date,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return IncidentsPaginationDto.from_dict(response.json())

    def get_enhanced_incidents_with_pagination_and_filters(
        self,
        limit: int,
        page: int,
        policy_name: str = "",
        rule_name: str = "",
        scan_id: str = "",
        project_name: str = "",
        branch: str = "",
        scanner: str = "",
        tags: str = "",
        scan_date_from: str = "",
        scan_date_to: str = "",
        sort: str = "",
        sort_field: str = "",
        sort_order: str = "",
    ) -> EnhancedIncidentsPaginationDTO:
        """Get tenant incidents (V2, with engine info) with pagination,
        filters, and sorting.

        Args:
            limit (int): Page size. Minimum 1.
            page (int): Page number (1-based).
            policy_name (str): Filter by policy name. Default: "".
            rule_name (str): Filter by rule name. Default: "".
            scan_id (str): Filter by scan UUID. Default: "".
            project_name (str): Filter by project name. Default: "".
            branch (str): Filter by branch. Default: "".
            scanner (str): Filter by scanner engine. Default: "".
            tags (str): Filter by policy tags. Default: "".
            scan_date_from (str): Filter by scan date range start. Default: "".
            scan_date_to (str): Filter by scan date range end. Default: "".
            sort (str): Sort direction. Default: "".
            sort_field (str): Field to sort by. Default: "".
            sort_order (str): Sort order. Default: "".

        Returns:
            EnhancedIncidentsPaginationDTO: Incidents on the page, and the
                filtered total count.
        """
        url = f"{self.base_url}/incidents/filters/v2"
        params = {
            "limit": limit,
            "page": page,
            "policyName": policy_name,
            "ruleName": rule_name,
            "scanId": scan_id,
            "projectName": project_name,
            "branch": branch,
            "scanner": scanner,
            "tags": tags,
            "scanDateFrom": scan_date_from,
            "scanDateTo": scan_date_to,
            "sort": sort,
            "sortField": sort_field,
            "sortOrder": sort_order,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return EnhancedIncidentsPaginationDTO.from_dict(response.json())

    def get_incident_results(
        self,
        incident_id: int,
        limit: int,
        page: int,
        issue: str = "",
        search: str = "",
        severity: str = "",
        sort_field: str = "severity",
        sort_order: str = "descend",
    ) -> IncidentResultsDTO:
        """Get the results underlying a specific incident.

        Args:
            incident_id (int): The incident ID.
            limit (int): Page size. Minimum 1.
            page (int): Page number (1-based).
            issue (str): Legacy issue-name filter. Ignored if `search` is
                also provided (a non-blank `search` takes precedence).
                Default: "".
            search (str): Free-text search over the issue name. Takes
                precedence over `issue` when non-blank. Default: "".
            severity (str): Filter by severity. Default: "".
            sort_field (str): Field to sort by. Default: "severity".
            sort_order (str): Sort order. Default: "descend".

        Returns:
            IncidentResultsDTO: Violation details common to all results,
                the results on the page, and the filtered total count.
        """
        url = f"{self.base_url}/incidents/{incident_id}/results"
        params = {
            "limit": limit,
            "page": page,
            "issue": issue,
            "search": search,
            "severity": severity,
            "sortField": sort_field,
            "sortOrder": sort_order,
        }
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return IncidentResultsDTO.from_dict(response.json())

    # =========================================================================
    # Internal data retention
    # =========================================================================

    def delete_data(self, limitation: int = None) -> bool:
        """Delete data from all services implementing IDataRetention.

        Args:
            limitation (int): Maximum number of records to delete, if given.

        Returns:
            bool: True if the request succeeded.
        """
        url = f"{self.base_url}/internal/data-retention"
        params = {"limitation": limitation}
        response = self.api_client.call_api(
            method="DELETE", url=url, params=params
        )
        return response.status_code in (200, 204)

    def delete_data_for_service(
        self, service_name: str, limitation: int = None
    ) -> bool:
        """Delete data from a specific service implementing IDataRetention.

        Args:
            service_name (str): The service's name.
            limitation (int): Maximum number of records to delete, if given.

        Returns:
            bool: True if the request succeeded.
        """
        url = f"{self.base_url}/internal/data-retention/{service_name}"
        params = {"limitation": limitation}
        response = self.api_client.call_api(
            method="DELETE", url=url, params=params
        )
        return response.status_code in (200, 204)


# ---- Module-level convenience functions ----

def get_tenant_policies() -> List[PolicyWebDto]:
    return PolicyManagerAPI().get_tenant_policies()


def create_policy(policy: PolicyWebDto) -> int:
    return PolicyManagerAPI().create_policy(policy=policy)


def delete_policies(ids: List[int]) -> bool:
    return PolicyManagerAPI().delete_policies(ids=ids)


def get_policy(policy_id: int) -> PolicyWebDto:
    return PolicyManagerAPI().get_policy(policy_id=policy_id)


def update_policy(policy_id: int, policy: PolicyWebDto) -> int:
    return PolicyManagerAPI().update_policy(policy_id=policy_id, policy=policy)


def delete_policy(policy_id: int) -> bool:
    return PolicyManagerAPI().delete_policy(policy_id=policy_id)


def get_policy_v2(policy_id: int) -> PolicyWebDto:
    return PolicyManagerAPI().get_policy_v2(policy_id=policy_id)


def update_policy_v2(policy_id: int, policy: PolicyWebDto) -> int:
    return PolicyManagerAPI().update_policy_v2(policy_id=policy_id, policy=policy)


def get_tenant_policies_with_pagination(
    limit: int, page: int, policy_name: str = ""
) -> PoliciesPaginationDto:
    return PolicyManagerAPI().get_tenant_policies_with_pagination(
        limit=limit, page=page, policy_name=policy_name
    )


def create_policy_v2(policy: PolicyWebDto) -> int:
    return PolicyManagerAPI().create_policy_v2(policy=policy)


def get_tenant_policies_with_pagination_v3(
    limit: int, page: int, policy_name: str = ""
) -> PoliciesPaginationDto:
    return PolicyManagerAPI().get_tenant_policies_with_pagination_v3(
        limit=limit, page=page, policy_name=policy_name
    )


def get_default_policy() -> Optional[PolicyShortWebDto]:
    return PolicyManagerAPI().get_default_policy()


def assign_projects_to_policy(
    policy_id: int, projects: ProjectsInPolicyDto
) -> int:
    return PolicyManagerAPI().assign_projects_to_policy(
        policy_id=policy_id, projects=projects
    )


def delete_projects_from_policy(
    policy_id: int, projects: ProjectsInPolicyDto
) -> bool:
    return PolicyManagerAPI().delete_projects_from_policy(
        policy_id=policy_id, projects=projects
    )


def pin_policy(policy_id: int, pin_policy_flag: bool) -> int:
    return PolicyManagerAPI().pin_policy(
        policy_id=policy_id, pin_policy=pin_policy_flag
    )


def get_tenant_projects() -> List[ProjectWebDto]:
    return PolicyManagerAPI().get_tenant_projects()


def get_projects_tags() -> List[str]:
    return PolicyManagerAPI().get_projects_tags()


def get_policy_violations(project_id: str, scan_id: str) -> PolicyViolationWebDto:
    return PolicyManagerAPI().get_policy_violations(
        project_id=project_id, scan_id=scan_id
    )


def get_evaluated_policies_by_scan_id_and_project_id(
    scan_id: str, ast_project_id: str
) -> PoliciesResultWebDto:
    return PolicyManagerAPI().get_evaluated_policies_by_scan_id_and_project_id(
        scan_id=scan_id, ast_project_id=ast_project_id
    )


def get_tenant_incidents() -> IncidentsPaginationDto:
    return PolicyManagerAPI().get_tenant_incidents()


def get_tenant_incidents_total_count() -> int:
    return PolicyManagerAPI().get_tenant_incidents_total_count()


def get_tenant_incidents_with_pagination(
    limit: int, page: int, incident_name: str = ""
) -> IncidentsPaginationDto:
    return PolicyManagerAPI().get_tenant_incidents_with_pagination(
        limit=limit, page=page, incident_name=incident_name
    )


def get_tenant_incidents_with_pagination_and_filters(
    limit: int,
    page: int,
    policy_name: str = "",
    rule_name: str = "",
    scan_id: str = "",
    project_name: str = "",
    branch: str = "",
    scan_date: str = "",
) -> IncidentsPaginationDto:
    return PolicyManagerAPI().get_tenant_incidents_with_pagination_and_filters(
        limit=limit,
        page=page,
        policy_name=policy_name,
        rule_name=rule_name,
        scan_id=scan_id,
        project_name=project_name,
        branch=branch,
        scan_date=scan_date,
    )


def get_enhanced_incidents_with_pagination_and_filters(
    limit: int,
    page: int,
    policy_name: str = "",
    rule_name: str = "",
    scan_id: str = "",
    project_name: str = "",
    branch: str = "",
    scanner: str = "",
    tags: str = "",
    scan_date_from: str = "",
    scan_date_to: str = "",
    sort: str = "",
    sort_field: str = "",
    sort_order: str = "",
) -> EnhancedIncidentsPaginationDTO:
    return PolicyManagerAPI().get_enhanced_incidents_with_pagination_and_filters(
        limit=limit,
        page=page,
        policy_name=policy_name,
        rule_name=rule_name,
        scan_id=scan_id,
        project_name=project_name,
        branch=branch,
        scanner=scanner,
        tags=tags,
        scan_date_from=scan_date_from,
        scan_date_to=scan_date_to,
        sort=sort,
        sort_field=sort_field,
        sort_order=sort_order,
    )


def get_incident_results(
    incident_id: int,
    limit: int,
    page: int,
    issue: str = "",
    search: str = "",
    severity: str = "",
    sort_field: str = "severity",
    sort_order: str = "descend",
) -> IncidentResultsDTO:
    return PolicyManagerAPI().get_incident_results(
        incident_id=incident_id,
        limit=limit,
        page=page,
        issue=issue,
        search=search,
        severity=severity,
        sort_field=sort_field,
        sort_order=sort_order,
    )


def delete_data(limitation: int = None) -> bool:
    return PolicyManagerAPI().delete_data(limitation=limitation)


def delete_data_for_service(service_name: str, limitation: int = None) -> bool:
    return PolicyManagerAPI().delete_data_for_service(
        service_name=service_name, limitation=limitation
    )
