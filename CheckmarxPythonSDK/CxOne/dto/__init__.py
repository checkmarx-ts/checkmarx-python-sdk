# encoding: utf-8
from .AddAssignmentRoles import AddAssignmentRoles
from .AiTrProcessResult import AiTrProcessResult
from .AiTrProcessStatusResponse import (
    AiTrProcessStatusResponse,
)
from .AiTriageTriggerRequest import (
    AiTriageTriggerRequest,
)
from .AiTriageTriggerResponse import (
    AiTriageTriggerResponse,
)
from .AiTriageVulnerability import (
    AiTriageVulnerability,
)
from .ApiSecCounters import ApiSecCounters
from .ScaRegistryConfigRequest import (
    ScaRegistryConfigRequest,
)
from .ScaRegistryConfigResponse import (
    ScaRegistryConfigResponse,
)
from .PackageActionValue import PackageActionValue
from .PackageAction import PackageAction
from .SupplyChainRiskAction import SupplyChainRiskAction
from .UpdatePackageStateBulkRequest import (
    BulkPackageEntry,
    UpdatePackageStateBulkRequest,
)
from .UpdatePackageStateRequest import (
    UpdatePackageStateRequest,
)
from .UpdateVulnerabilitiesBulkRequest import (
    BulkVulnerabilityEntry,
    UpdateVulnerabilitiesBulkRequest,
)
from .UpdateVulnerabilityRequest import (
    UpdateVulnerabilityRequest,
)
from .UpdateSupplyChainRisksBulkRequest import (
    BulkSupplyChainRiskEntry,
    UpdateSupplyChainRisksBulkRequest,
)
from .UpdateSupplyChainRiskRequest import (
    UpdateSupplyChainRiskRequest,
)
from .ScaProjectWithConfigurations import (
    ScaProjectWithConfigurations,
)
from .ScaTagWithConfigurations import (
    ScaTagWithConfigurations,
)
from .ScaRegistryConfiguration import (
    ScaRegistryConfiguration,
)
from .Application import Application
from .ApplicationInput import ApplicationInput
from .ApplicationsCollection import ApplicationsCollection
from .Assignment import Assignment
from .AssignmentInput import AssignmentInput
from .AssignmentsForResource import (
    AssignmentsForResource,
)
from .AssignmentsWithBaseRoles import (
    AssignmentsWithBaseRoles,
)
from .AstIdWithName import AstIdWithName
from .AstUser import AstUser
from .AsyncRequestResponse import AsyncRequestResponse
from .AuditEvent import AuditEvent
from .AuditEventLink import AuditEventLink
from .AuditEvents import AuditEvents
from .AuditQuery import AuditQuery
from .BaseRolesRequest import BaseRolesRequest
from .BaseRolesResponse import BaseRolesResponse
from .BflTree import BflTree
from .ByorJob import ByorJob
from .ByorJobPatchRequest import ByorJobPatchRequest
from .Category import Category
from .CategoryType import CategoryType
from .ChangeDetails import ChangeDetails
from .Client import Client
from .ClientsWithResourcesResponse import (
    ClientsWithResourcesResponse,
)
from .ClientWithResource import ClientWithResource
from .CloudInsightAccount import CloudInsightAccount
from .CloudInsightAccountLog import CloudInsightAccountLog
from .CloudInsightContainer import CloudInsightContainer
from .CloudInsightCreateEnrichAccount import CloudInsightCreateEnrichAccount
from .CloudInsightEnrichAccount import CloudInsightEnrichAccount
from .CommentJSON import CommentJSON
from .CompilationResponse import CompilationResponse
from .ComplianceSummary import ComplianceSummary
from .ContributorInsights import ContributorInsights
from .Contributors import Contributors
from .ContributorScmInsights import ContributorScmInsights
from .ContributorUnfamiliarProjects import ContributorUnfamiliarProjects
from .CreatedApplication import CreatedApplication
from .CreateRoleRequest import CreateRoleRequest
from .CredentialRepresentation import CredentialRepresentation
from .Credentials import Credentials
from .CustomState import CustomState
from .DastAlertRiskLevel import DastAlertRiskLevel
from .DastApplication import DastApplication
from .DastAuthSettings import DastAuthSettings
from .DastAuthSuccess import DastAuthSuccess
from .DastAutomationAction import DastAutomationAction
from .DastAutomationEngine import DastAutomationEngine
from .DastAutomationScript import DastAutomationScript
from .DastAutomationScriptType import DastAutomationScriptType
from .DastAutomationType import DastAutomationType
from .DastCliSettings import DastCliSettings
from .DastConfigFileSettings import DastConfigFileSettings
from .DastCustomHeader import DastCustomHeader
from .DastEnvironment import DastEnvironment
from .DastEnvironmentFilter import DastEnvironmentFilter
from .DastEnvironmentGroupCount import DastEnvironmentGroupCount
from .DastEnvironmentInput import DastEnvironmentInput
from .DastEnvironmentSettings import DastEnvironmentSettings
from .DastEnvironmentUpdate import DastEnvironmentUpdate
from .DastEnvironmentsCollection import DastEnvironmentsCollection
from .DastGroupBy import DastGroupBy
from .DastLastRiskRating import DastLastRiskRating
from .DastPollHeader import DastPollHeader
from .DastResult import DastResult
from .DastResultChangelogEntry import DastResultChangelogEntry
from .DastResultDetail import DastResultDetail
from .DastResultNote import DastResultNote
from .DastResultSeverity import DastResultSeverity
from .DastResultState import DastResultState
from .DastResultStatus import DastResultStatus
from .DastResultsChangelogInput import DastResultsChangelogInput
from .DastResultsChangelogType import DastResultsChangelogType
from .DastResultsCollection import DastResultsCollection
from .DastResultsFilter import DastResultsFilter
from .DastResultsGroupBy import DastResultsGroupBy
from .DastResultsGroupCount import DastResultsGroupCount
from .DastResultsSortBy import DastResultsSortBy
from .DastRunScanInput import DastRunScanInput
from .DastScan import DastScan
from .DastScanAuth import DastScanAuth
from .DastScanAuthParameters import DastScanAuthParameters
from .DastScanAuthVerification import DastScanAuthVerification
from .DastScanConfig import DastScanConfig
from .DastScanFilter import DastScanFilter
from .DastScanGroupBy import DastScanGroupBy
from .DastScanGroupCount import DastScanGroupCount
from .DastScanGroupFilter import DastScanGroupFilter
from .DastScanInsight import DastScanInsight
from .DastScanOption import DastScanOption
from .DastScanOptions import DastScanOptions
from .DastScanSortBy import DastScanSortBy
from .DastScanStatus import DastScanStatus
from .DastScanType import DastScanType
from .DastScanUpdate import DastScanUpdate
from .DastScanUser import DastScanUser
from .DastScansCollection import DastScansCollection
from .DastSessionManagement import DastSessionManagement
from .DastSessionManagementHeader import DastSessionManagementHeader
from .DastSortBy import DastSortBy
from .DastSortOrder import DastSortOrder
from .DastTotpField import DastTotpField
from .DastTunnelState import DastTunnelState
from .DastUserCredentials import DastUserCredentials
from .DebugMessage import DebugMessage
from .DebugMessageResponse import DebugMessageResponse
from .DefaultConfig import DefaultConfig
from .DefaultConfigOut import DefaultConfigOut
from .EffectivePermissionsForResourceResponse import (
    EffectivePermissionsForResourceResponse,
)
from .EngineData import EngineData
from .EngineMetrics import EngineMetrics
from .EntitiesForExtendedResponse import (
    EntitiesForExtendedResponse,
)
from .EntityRolesRequest import EntityRolesRequest
from .EntityType import EntityType
from .Error import Error
from .ExecutionResponse import ExecutionResponse
from .FederatedIdentityRepresentation import FederatedIdentityRepresentation
from .FileInfo import FileInfo
from .Flag import Flag
from .UsersWithResourcesResponse import (
    UsersWithResourcesResponse,
)
from .Git import Git
from .GPTMessage import GPTMessage
from .Group import Group
from .GroupRepresentation import GroupRepresentation
from .GroupsResponse import GroupsResponse
from .GroupsWithResourcesResponse import (
    GroupsWithResourcesResponse,
)
from .GroupWithResource import GroupWithResource
from .ImportItem import ImportItem
from .ImportItemWithLogs import ImportItemWithLogs
from .ImportRequest import ImportRequest
from .ImportResults import ImportResults
from .InternalClient import InternalClient
from .InternalGroup import InternalGroup
from .InternalUser import InternalUser
from .KicsResult import KicsResult
from .KicsResultCollection import KicsResultCollection
from .LanguageSummary import LanguageSummary
from .LogItem import LogItem
from .Metadata import Metadata
from .MethodInfo import MethodInfo
from .MethodParameter import MethodParameter
from .MultipleAssignmentInput import MultipleAssignmentInput
from .PaginatedAccountLogsListResponse import PaginatedAccountLogsListResponse
from .PaginatedAccountsListResponse import PaginatedAccountsListResponse
from .PaginatedContainersListResponse import PaginatedContainersListResponse
from .PaginatedResourcesList import PaginatedResourcesList
from .Permission import Permission
from .PlatformSummary import PlatformSummary
from .Predicate import Predicate
from .PredicateHistory import PredicateHistory
from .PredicateInitialValues import PredicateInitialValues
from .PredicateHistoryResponse import PredicateHistoryResponse
from .PredicateWithCommentJSON import PredicateWithCommentJSON
from .PredicateWithCommentsJSON import PredicateWithCommentsJSON
from .Preset import Preset
from .PresetPaged import PresetPaged
from .PresetSummary import PresetSummary
from .Project import Project
from .ProjectCounter import ProjectCounter
from .ProjectInput import ProjectInput
from .ScheduleInput import ScheduleInput
from .ProjectResponseCollection import ProjectResponseCollection
from .ProjectResponseModel import ProjectResponseModel
from .ProjectsCollection import ProjectsCollection
from .ProjectSettings import ProjectSettings
from .Property import Property
from .ProtocolMappersRepresentation import (
    ProtocolMappersRepresentation,
)
from .Queries import Queries
from .QueriesResponse import QueriesResponse
from .QueriesTree import QueriesTree
from .Query import Query
from .QueryBuilderMessage import QueryBuilderMessage
from .QueryBuilderPrompt import QueryBuilderPrompt
from .QueryDescription import QueryDescription
from .QueryDescriptionSampleCode import QueryDescriptionSampleCode
from .QueryDetails import QueryDetails
from .QueryRequest import QueryRequest
from .QueryResponse import QueryResponse
from .QueryResult import QueryResult
from .QuerySearch import QuerySearch
from .QuerySummary import QuerySummary
from .RequestStatus import RequestStatus
from .RequestStatusDetectLanguages import RequestStatusDetectLanguages
from .RequestStatusNotReady import RequestStatusNotReady
from .Resource import Resource
from .ResourcesResponse import ResourcesResponse
from .ResourceType import ResourceType
from .Result import Result
from .ResultNode import ResultNode
from .ResultResponse import ResultResponse
from .ResultsResponse import ResultsResponse
from .ResultsSummary import ResultsSummary
from .ResultsSummaryTree import ResultsSummaryTree
from .RiskLevel import RiskLevel
from .Role import Role
from .RoleWithDetails import RoleWithDetails
from .Rule import Rule
from .RuleInput import RuleInput
from .SastResult import SastResult
from .SastScan import SastScan
from .SastStatus import SastStatus
from .ScaContainersCounters import ScaContainersCounters
from .ScaCounters import ScaCounters
from .Scan import Scan
from .ScanConfig import ScanConfig
from .ScanEngineVersion import ScanEngineVersion
from .ScanInfo import ScanInfo
from .ScanInfoCollection import ScanInfoCollection
from .ScanInput import ScanInput
from .Scanner import Scanner
from .ScanParameter import ScanParameter
from .ScansCollection import ScansCollection
from .ScaPackageCounters import ScaPackageCounters
from .Scm import Scm
from .SCMImportInput import SCMImportInput
from .ScmOrganization import ScmOrganization
from .ScmProject import ScmProject
from .Session import Session
from .SessionRequest import SessionRequest
from .SessionResponse import SessionResponse
from .Sessions import Sessions
from .SeverityCounter import SeverityCounter
from .SeveritySummary import SeveritySummary
from .SinkFileSummary import SinkFileSummary
from .SinkNodeSummary import SinkNodeSummary
from .SocialLinkRepresentation import SocialLinkRepresentation
from .SourceFileSummary import SourceFileSummary
from .SourceNodeSummary import SourceNodeSummary
from .SourcesTree import SourcesTree
from .StartEnrich import StartEnrich
from .StatusDetails import StatusDetails
from .SubCheck import SubCheck
from .SubsetScan import SubsetScan
from .TaskInfo import TaskInfo
from .TenantOverview import TenantOverview
from .TimeStamp import TimeStamp
from .TotalCounters import TotalCounters
from .Tree import Tree
from .TriageRequest import TriageRequest
from .TriageResponse import TriageResponse
from .Upload import Upload
from .User import User
from .UserConsentRepresentation import UserConsentRepresentation
from .UserFederationMapperRepresentation import UserFederationMapperRepresentation
from .UserFederationProviderRepresentation import UserFederationProviderRepresentation
from .UserProfileAttributeGroupMetadata import UserProfileAttributeGroupMetadata
from .UserProfileAttributeMetadata import UserProfileAttributeMetadata
from .UserProfileMetadata import UserProfileMetadata
from .UserRepresentation import UserRepresentation
from .UsersWithResourcesResponse import (
    UsersWithResourcesResponse,
)
from .UserWithResource import UserWithResource
from .VersionsOut import VersionsOut
from .WebError import WebError
from .WebHook import WebHook
from .WebHookConfig import WebHookConfig
from .WebHookEvent import WebHookEvent
from .WebHookInput import WebHookInput
from .WebHooksCollection import WebHooksCollection
from .WorkspaceQuery import WorkspaceQuery
