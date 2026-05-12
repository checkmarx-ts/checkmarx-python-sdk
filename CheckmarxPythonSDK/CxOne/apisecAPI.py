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

    @classmethod
    def from_dict(cls, item: dict) -> "ApiRequestParameter":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            type=item.get("type"),
            location=item.get("location"),
            origin=item.get("origin"),
            model=item.get("model"),
            content_type=item.get("content_type"),
            pii=item.get("pii"),
        )


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

    @classmethod
    def from_dict(cls, item: dict) -> "ApiResponseParameter":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            type=item.get("type"),
            code=item.get("code"),
            origin=item.get("origin"),
            model=item.get("model"),
            content_type=item.get("content_type"),
            pii=item.get("pii"),
        )


@dataclass
class ApiResponsePii:
    name: str = None
    location: str = None
    count: int = 0
    origin: List[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ApiResponsePii":
        return cls(
            name=item.get("name"),
            location=item.get("location"),
            count=item.get("count", 0),
            origin=item.get("origin"),
        )


@dataclass
class Parameter:
    request_parameters: List[ApiRequestParameter] = None
    response_parameters: List[ApiResponseParameter] = None
    pii: List[ApiResponsePii] = None
    api_origins: List[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Parameter":
        return cls(
            request_parameters=[
                ApiRequestParameter.from_dict(p)
                for p in (item.get("request_parameters") or [])
            ],
            response_parameters=[
                ApiResponseParameter.from_dict(p)
                for p in (item.get("response_parameters") or [])
            ],
            pii=[ApiResponsePii.from_dict(p) for p in (item.get("pii") or [])],
            api_origins=item.get("api_origins"),
        )


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

    @classmethod
    def from_dict(cls, item: dict) -> "RiskDetailResponse":
        return cls(
            vulnerability=item.get("vulnerability"),
            status=item.get("status"),
            source_node=item.get("source_node"),
            source_file=item.get("source_file"),
            total_pii=item.get("total_pii", 0),
            line_number=item.get("line_number"),
            description=item.get("description"),
            actual_value=item.get("actual_value"),
            expected_value=item.get("expected_value"),
            state=item.get("state"),
            similarity_id=item.get("similarity_id"),
            scan_id=item.get("scan_id"),
        )


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

    @classmethod
    def from_dict(cls, item: dict) -> "Risk":
        return cls(
            risk_id=item.get("risk_id"),
            api_id=item.get("api_id"),
            severity=item.get("severity"),
            name=item.get("name"),
            status=item.get("status"),
            http_method=item.get("http_method"),
            url=item.get("url"),
            origin=item.get("origin"),
            documented=item.get("documented"),
            authenticated=item.get("authenticated"),
            discovery_date=item.get("discovery_date"),
            scan_id=item.get("scan_id"),
            sast_risk_id=item.get("sast_risk_id"),
            project_id=item.get("project_id"),
            state=item.get("state"),
        )


@dataclass
class RiskResponse:
    entries: List[Risk] = None
    total_records: str = None
    total_pages: str = None
    has_previous: bool = None
    has_next: bool = None
    next_page_number: int = None
    previous_page_number: Any = None

    @classmethod
    def from_dict(cls, item: dict) -> "RiskResponse":
        return cls(
            entries=[Risk.from_dict(e) for e in (item.get("entries") or [])],
            total_records=item.get("total_records"),
            total_pages=item.get("total_pages"),
            has_previous=item.get("has_previous"),
            has_next=item.get("has_next"),
            next_page_number=item.get("next_page_number"),
            previous_page_number=item.get("previous_page_number"),
        )


@dataclass
class GroupTypes:
    top_level_group_value: str = None
    total_records: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "GroupTypes":
        return cls(
            top_level_group_value=item.get("top_level_group_value"),
            total_records=item.get("total_records"),
        )


@dataclass
class GroupResponse:
    groups: List[GroupTypes] = None
    total_records: str = None
    total_pages: str = None
    has_previous: bool = None
    has_next: bool = None
    next_page_number: int = None
    previous_page_number: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "GroupResponse":
        return cls(
            groups=[GroupTypes.from_dict(g) for g in (item.get("groups") or [])],
            total_records=item.get("total_records"),
            total_pages=item.get("total_pages"),
            has_previous=item.get("has_previous"),
            has_next=item.get("has_next"),
            next_page_number=item.get("next_page_number"),
            previous_page_number=item.get("previous_page_number"),
        )


@dataclass
class ScanRisksOriginsItemResult:
    name: str = None
    count: int = 0

    @classmethod
    def from_dict(cls, item: dict) -> "ScanRisksOriginsItemResult":
        return cls(
            name=item.get("name"),
            count=item.get("count", 0),
        )


@dataclass
class ScanRisksOriginsResult:
    entries: List[ScanRisksOriginsItemResult] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScanRisksOriginsResult":
        if isinstance(item, list):
            entries = [ScanRisksOriginsItemResult.from_dict(e) for e in item]
        else:
            entries = [
                ScanRisksOriginsItemResult.from_dict(e)
                for e in (item.get("entries") or [])
            ]
        return cls(entries=entries)


@dataclass
class RisksDistribution:
    origin: str = None
    total: int = 0

    @classmethod
    def from_dict(cls, item: dict) -> "RisksDistribution":
        return cls(
            origin=item.get("origin"),
            total=item.get("total", 0),
        )


@dataclass
class RisksDistributionState:
    state: str = None
    total: int = 0

    @classmethod
    def from_dict(cls, item: dict) -> "RisksDistributionState":
        return cls(
            state=item.get("state"),
            total=item.get("total", 0),
        )


@dataclass
class RisksOverview:
    api_count: int = 0
    total_risks_count: int = 0
    risks: List[int] = None
    risk_distribution: List[RisksDistribution] = None
    risks_by_state: List[RisksDistributionState] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RisksOverview":
        return cls(
            api_count=item.get("api_count", 0),
            total_risks_count=item.get("total_risks_count", 0),
            risks=item.get("risks"),
            risk_distribution=[
                RisksDistribution.from_dict(d)
                for d in (item.get("risk_distribution") or [])
            ],
            risks_by_state=[
                RisksDistributionState.from_dict(s)
                for s in (item.get("risks_by_state") or [])
            ],
        )


@dataclass
class RiskType:
    name: str = None  # Allowed values: code, documentation
    count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "RiskType":
        return cls(
            name=item.get("name"),
            count=item.get("count"),
        )


@dataclass
class RisksTypes:
    entries: List[RiskType] = None
    origin: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "RisksTypes":
        return cls(
            entries=[RiskType.from_dict(e) for e in (item.get("entries") or [])],
            origin=item.get("origin"),
        )


@dataclass
class RisksTypesResponse:
    risks: List[RisksTypes] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RisksTypesResponse":
        return cls(
            risks=[RisksTypes.from_dict(r) for r in (item.get("risks") or [])],
        )


@dataclass
class ScanSensitiveData:
    count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScanSensitiveData":
        return cls(count=item.get("count"))


@dataclass
class ScanUndocumentedApis:
    count: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScanUndocumentedApis":
        return cls(count=item.get("count"))


@dataclass
class ApiSecRisksOverview:
    api_count: int = 0
    total_risks_count: int = 0
    risks: List[int] = None
    risk_distribution: List[RisksDistribution] = None
    risks_by_state: List[RisksDistributionState] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ApiSecRisksOverview":
        return cls(
            api_count=item.get("api_count", 0),
            total_risks_count=item.get("total_risks_count", 0),
            risks=item.get("risks"),
            risk_distribution=[
                RisksDistribution.from_dict(d)
                for d in (item.get("risk_distribution") or [])
            ],
            risks_by_state=[
                RisksDistributionState.from_dict(s)
                for s in (item.get("risks_by_state") or [])
            ],
        )


@dataclass
class ScanMetadata:
    value: str = None
    label: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScanMetadata":
        return cls(
            value=item.get("value"),
            label=item.get("label"),
        )


@dataclass
class ScanMetadataResponse:
    column: str = None
    options: List[ScanMetadata] = None
    grouping: bool = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScanMetadataResponse":
        return cls(
            column=item.get("column"),
            options=[ScanMetadata.from_dict(o) for o in (item.get("options") or [])],
            grouping=item.get("grouping"),
        )


class ApiSecAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/apisec/static/api"
        )

    def get_risk_summary_by_origin(self, scan_id: str) -> ScanRisksOriginsResult:
        """
        Get a summary of the number of API Security risks identified in
        each of the data sources. Possible data sources are, code and
        documentation (i.e., Swagger)
        """
        url = f"{self.base_url}/scan/{scan_id}/risks-origin"
        response = self.api_client.call_api(method="GET", url=url)
        return ScanRisksOriginsResult.from_dict(response.json())

    def get_scan_apisec_risk_overview(self, scan_id: str) -> ApiSecRisksOverview:
        """
        Get an overview of the number of APIs identified by a particular
        scan, and the number of associated risks.
        """
        url = f"{self.base_url}/scan/{scan_id}/risks-overview"
        response = self.api_client.call_api(method="GET", url=url)
        return ApiSecRisksOverview.from_dict(response.json())

    def get_all_risk_types(self, scan_id: str) -> RisksTypesResponse:
        """
        Get info about the top 10 API Security risk types identified in a
        particular scan.

        Args:
            scan_id (str)

        Returns:
            RisksTypesResponse
        """
        url = f"{self.base_url}/scan/{scan_id}/risks-types"
        response = self.api_client.call_api(method="GET", url=url)
        return RisksTypesResponse.from_dict(response.json())

    def get_number_of_sensitive_data_apis(self, scan_id: str) -> ScanSensitiveData:
        """
        Get the number of APIs that include sensitive data (e.g., passwords,
        private info etc.) that were identified in a particular scan.

        Args:
            scan_id (str)

        Returns:
            ScanSensitiveData
        """
        url = f"{self.base_url}/scan/{scan_id}/sensitive-data"
        response = self.api_client.call_api(method="GET", url=url)
        return ScanSensitiveData.from_dict(response.json())

    def get_number_of_undocumented_apis(self, scan_id: str) -> ScanUndocumentedApis:
        """
        Get the number of APIs identified in your source code that aren't
        in your documentation, for a particular scan.

        Args:
            scan_id (str)

        Returns:
            ScanUndocumentedApis
        """
        url = f"{self.base_url}/scan/{scan_id}/undocumented-apis"
        response = self.api_client.call_api(method="GET", url=url)
        return ScanUndocumentedApis.from_dict(response.json())

    def get_all_api_scan_metadata(self) -> List[ScanMetadataResponse]:
        """
        Get all api scan Metadata

        Returns:
            List[ScanMetadataResponse]
        """
        url = f"{self.base_url}/scan/metadata"
        response = self.api_client.call_api(method="GET", url=url)
        return [ScanMetadataResponse.from_dict(item) for item in response.json()]

    def get_risk_detail_by_risk_id(self, risk_id: str) -> RiskDetailResponse:
        """
        Get risk detail by id

        Args:
            risk_id (str): Risk id

        Returns:
            RiskDetailResponse
        """
        url = f"{self.base_url}/risks/risk/{risk_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return RiskDetailResponse.from_dict(response.json())

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
            scan_id (str):
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
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return RiskResponse.from_dict(response.json())

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
        the specified category (e.g., for severity, returns number of critical,
        high, medium, low)

        Args:
            scan_id (str):
            group_column (str):
            filtering (str):
            page (int):
            per_page (int):
            searching (str):
            sorting (str):

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
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return GroupResponse.from_dict(response.json())

    def get_api_parameters(self, api_id: str) -> Parameter:
        """
        Args:
            api_id (str): Specify the unique identifier of the API

        Returns:
            Parameter
        """
        url = f"{self.base_url}/risks/parameters"
        params = {"api_id": api_id}
        response = self.api_client.call_api(method="GET", url=url, params=params)
        return Parameter.from_dict(response.json())


def get_scan_apisec_risk_overview(scan_id: str) -> ApiSecRisksOverview:
    return ApiSecAPI().get_scan_apisec_risk_overview(scan_id)
