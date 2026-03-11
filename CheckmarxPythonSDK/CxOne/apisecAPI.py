import logging
from typing import List, Any
from dataclasses import dataclass
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration

logger = logging.getLogger(__name__)

@dataclass 
class ApiRequestParameter:
    id: str = None
    name: str = None
    type: str = None
    location: str = None
    origin: List[str] = None
    model: str = None
    content_type: List[str] = None
    pii: List[str] = None


@dataclass 
class ApiResponseParameter:
    id: str = None
    name: str = None
    type: str = None
    code: int = None
    origin: List[str] = None
    model: str = None
    content_type: List[str] = None
    pii: List[str] = None


@dataclass
class ApiResponsePii:
    name: str = None
    location: str = None
    count: int = 0
    origin: List[str] = None


@dataclass
class Parameter:
    request_parameters: List[ApiRequestParameter] = None
    response_parameters: List[ApiResponseParameter] = None
    pii: List[ApiResponsePii] = None
    api_origins: List[str] = None

@dataclass
class RiskDetailResponse:
    vulnerability: str = None
    status: str = None
    source_node: str = None
    source_file: str = None
    total_pii: int = 0
    line_number: int = None
    description: str = None
    actual_value: str = None
    expected_value: str = None
    state: str = None
    similarity_id: str = None
    scan_id: str = None


@dataclass
class Risk:
    risk_id: str = None
    api_id: str = None
    severity: str = None
    name: str = None
    status: str = None
    http_method: str = None
    url: str = None
    origin: str = None
    documented: bool = None
    authenticated: bool = None
    discovery_date: str = None
    scan_id: str = None
    sast_risk_id: str = None
    project_id: str = None
    state: str = None


@dataclass
class RiskResponse:
    entries: List[Risk] = None
    total_records: str = None
    total_pages: str = None
    has_previous: bool = None
    has_next: bool = None
    next_page_number: int = None
    previous_page_number: Any = None


@dataclass 
class GroupTypes:
    top_level_group_value: str = None
    total_records: int = None


@dataclass
class GroupResponse:
    groups: List[GroupTypes] = None
    total_records: str = None
    total_pages: str = None
    has_previous: bool = None
    has_next: bool = None
    next_page_number: int = None
    previous_page_number: int = None


@dataclass
class ScanRisksOriginsItemResult:
    name: str = None
    count: int = 0


@dataclass
class ScanRisksOriginsResult:
    entries: List[ScanRisksOriginsItemResult] = None


@dataclass
class RisksDistribution:
    origin: str = None
    total: int = 0


@dataclass
class RisksDistributionState:
    state: str = None
    total: int = 0


@dataclass
class RisksOverview:
    api_count: int = 0
    total_risks_count: int = 0
    risks: List[int] = None
    risk_distribution: List[RisksDistribution] = None
    risks_by_state: List[RisksDistributionState] = None


@dataclass
class RiskType:
    name: str = None # Allowed values: code, documentation
    count: int = None


@dataclass
class RisksTypes:
    entries: List[RiskType] = None
    origin: str = None


@dataclass
class RisksTypesResponse:
    risks: List[RisksTypes] = None

@dataclass
class ScanSensitiveData:
    count: int = None


@dataclass
class ScanUndocumentedApis:
    count: int = None


@dataclass
class ApiSecRisksOverview:
    api_count: int = 0
    total_risks_count: int = 0
    risks: List[int] = None
    risk_distribution: List[RisksDistribution] = None
    risks_by_state: List[RisksDistributionState] = None


@dataclass
class ScanMetadata:
    value: str = None
    label: str = None


@dataclass 
class ScanMetadataResponse:
    column: str = None
    options: List[ScanMetadata] = None
    grouping: bool = None


class ApiSecAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/apisec/static/api"
        )

    def get_risk_summary_by_origin(
            self, 
            scan_id: str
        ) -> ScanRisksOriginsResult:
        """
        Get a summary of the number of API Security risks identified in
        each of the data sources. Possible data sources are, code and 
        documentation (i.e., Swagger)
        """
        url = f"{self.base_url}/scan/{scan_id}/risks-origin"
        response = self.api_client.call_api(
            method="GET",
            url=url
        )
        data = response.json()
        # 检查返回数据的格式
        if isinstance(data, dict):
            return ScanRisksOriginsResult(**data)
        elif isinstance(data, list):
            # 如果返回的是列表，创建一个包含该列表的ScanRisksOriginsResult
            return ScanRisksOriginsResult(entries=data)
        else:
            # 其他情况，返回空结果
            return ScanRisksOriginsResult(entries=[])
        

    def get_scan_apisec_risk_overview(
            self, 
            scan_id: str
        ) -> ApiSecRisksOverview:
        """
        Get an overview of the number of APIs identified by a particular 
        scan, and the number of associated risks.
        """
        url = f"{self.base_url}/scan/{scan_id}/risks-overview"
        response = self.api_client.call_api(
            method="GET",
            url=url
        )
        return ApiSecRisksOverview(**response.json())

    def get_all_risk_types(
            self,
            scan_id: str,
        ) -> RisksTypesResponse:
        """
        Get info about the top 10 API Security risk types identified in a 
        particular scan.
        
        Args:
            scan_id (str)
        
        Returns:
            RisksTypesResponse
        """
        url = f"{self.base_url}/scan/{scan_id}/risks-types"
        response = self.api_client.call_api(
            method="GET",
            url=url
        )
        return RisksTypesResponse(**response.json())
    
    def get_number_of_sensitive_data_apis(
            self,
            scan_id: str,
        ) -> ScanSensitiveData:
        """
        Get the nuber of APIs that include sensitive data (e.g., passwords, 
        private info etc.) that were identified in a particular scan.

        Args:
            scan_id (str)
        
        Returns:
            ScanSensitiveData

        """
        url = f"{self.base_url}/scan/{scan_id}/sensitive-data"
        response = self.api_client.call_api(
            method="GET",
            url=url
        )
        return ScanSensitiveData(**response.json())
    
    def get_number_of_undocumented_apis(
            self,
            scan_id: str,
        ) -> ScanUndocumentedApis:
        """
        Get the number of APIs identified in your source code that aren't 
        in your documentation, for a particular scan.

        Args:
            scan_id (str)
        
        Returns:
            ScanUndocumentedApis

        """
        url = f"{self.base_url}/scan/{scan_id}/undocumented-apis"
        response = self.api_client.call_api(
            method="GET",
            url=url
        )
        return ScanUndocumentedApis(**response.json())

    def get_all_api_scan_metadata(
            self
        ) -> List[ScanMetadataResponse]:
        """
        Get all api scan Metadata

        Returns:
            List[ScanMetadataResponse]
        """
        url = f"{self.base_url}/scan/metadata"
        response = self.api_client.call_api(
            method="GET",
            url=url
        )
        print(response.json())
        return [ScanMetadataResponse(**item) for item in response.json()]

    def get_risk_detail_by_risk_id(
            self,
            risk_id: str
        ) -> RiskDetailResponse:
        """
        Get risk detail by id
        Args:
            risk_id (str): Risk id
        Returns:
            RiskDetailResponse
        """
        url = f"{self.base_url}/risks/risk/{risk_id}"
        response = self.api_client.call_api(
            method="GET",
            url=url
        )
        return RiskDetailResponse(**response.json())

    def get_api_security_risks_by_scan_id(
            self,
            scan_id: str,
            filtering: str = None,
            page: int = None,
            per_page: int = None,
            searching: str = None,
            sorting: str = None,
        ) -> RiskResponse:
        """
        Get detailed info about each API Security risk instance that was 
        identified in a particular scan.

        Args:
            filtering (str): Filter by fields (e.g., 
                filter=[{"column":"name","values": "Absolute_Path_Traversal", 
                "operator":"eq"}]
            page (int): Page number requested
            per_page (int): Number of items per page
            searching (str): Full text search (e.g., searching=low)
            sorting (str): Sorting direction (e.g., sort=[{"column":"name",
                "order": "asc"}])
        Returns:
            RiskResponse
        """
        url = f"{self.base_url}/risks/{scan_id}"
        params = {
            "filter": filtering,
            "page": page,
            "per_page": per_page,
            "searching": searching,
            "sorting": sorting,
        }
        response = self.api_client.call_api(
            method="GET",
            url=url,
            params=params,
        )
        return RiskResponse(**response.json())

    def get_grouped_risk_summary(
            self,
            scan_id: str,
            group_column: str,
            filtering: str = None,
            page: int = None,
            per_page: int = None,
            searching: str = None,
            sorting: str = None,
        ) -> GroupResponse:
        """
        Get a summary of the number of API Security risks of each value for 
        the specified catgory (e.g., for severity, returns number of critical,
        high, medium, low)

        Args:

        Returns:
            GroupResponse
        """
        url = f"{self.base_url}/risks/{scan_id}/group/{group_column}"
        params = {
            "filter": filtering,
            "page": page,
            "per_page": per_page,
            "searching": searching,
            "sorting": sorting,
        }
        response = self.api_client.call_api(
            method="GET",
            url=url,
            params=params,
        )
        print(response.json())
        return GroupResponse(**response.json())

    def get_api_parameters(
            self,
            api_id: str
        ) -> Parameter:
        """

        Args:
            api_id (str): Specify the unique identifier of the API

        Returns:
            Parameter
        """
        url = f"{self.base_url}/risks/parameters"
        params = {
            "api_id": api_id,
        }
        response = self.api_client.call_api(
            method="GET",
            url=url,
            params=params,
        )
        return Parameter(**response.json())

def get_scan_apisec_risk_overview(scan_id: str) -> ApiSecRisksOverview:
    return ApiSecAPI().get_scan_apisec_risk_overview(scan_id)
