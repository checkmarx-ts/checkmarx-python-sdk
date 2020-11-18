def construct_project_data(item):
    """

    Args:
        item (dict):

    Returns:
        dict
    """
    return {
            "Id": item.get("Id"),
            "Name": item.get("Name"),
            "IsPublic": item.get("IsPublic"),
            "Description": item.get("Description"),
            "CreatedDate": item.get("CreatedDate"),
            "OwnerId": item.get("OwnerId"),
            "OwningTeamId": item.get("OwningTeamId"),
            "EngineConfigurationId": item.get("EngineConfigurationId"),
            "IssueTrackingSettings": item.get("IssueTrackingSettings"),
            "SourcePath": item.get("SourcePath"),
            "SourceProviderCredentials": item.get("SourceProviderCredentials"),
            "ExcludedFiles": item.get("ExcludedFiles"),
            "ExcludedFolders": item.get("ExcludedFolders"),
            "OriginClientTypeId": item.get("OriginClientTypeId"),
            "PresetId": item.get("PresetId"),
            "LastScanId": item.get("LastScanId"),
            "TotalProjectScanCount": item.get("TotalProjectScanCount"),
            "SchedulingExpression": item.get("SchedulingExpression"),
        }


def construct_scan_data(item):
    """

    Args:
        item (dict):

    Returns:
        dict
    """
    return {
        "Id": item.get("Id"),
        "SourceId": item.get("SourceId"),
        "Comment": item.get("Comment"),
        "IsIncremental": item.get("IsIncremental"),
        "ScanType": item.get("ScanType"),
        "Origin": item.get("Origin"),
        "OwnerId": item.get("OwnerId"),
        "OwningTeamId": item.get("OwningTeamId"),
        "InitiatorName": item.get("InitiatorName"),
        "ProjectName": item.get("ProjectName"),
        "PresetName": item.get("PresetName"),
        "TeamName": item.get("TeamName"),
        "Path": item.get("Path"),
        "FileCount": item.get("FileCount"),
        "LOC": item.get("LOC"),
        "FailedLOC": item.get("FailedLOC"),
        "ProductVersion": item.get("ProductVersion"),
        "IsForcedScan": item.get("IsForcedScan"),
        "ScanRequestedOn": item.get("ScanRequestedOn"),
        "QueuedOn": item.get("QueuedOn"),
        "EngineStartedOn": item.get("EngineStartedOn"),
        "EngineFinishedOn": item.get("EngineFinishedOn"),
        "ScanCompletedOn": item.get("ScanCompletedOn"),
        "ScanDuration": item.get("ScanDuration"),
        "ProjectId": item.get("ProjectId"),
        "EngineServerId": item.get("EngineServerId"),
        "PresetId": item.get("PresetId"),
        "QueryLanguageVersionId": item.get("QueryLanguageVersionId"),
        "ScannedLanguageIds": item.get("ScannedLanguageIds"),
        "TotalVulnerabilities": item.get("TotalVulnerabilities"),
        "High": item.get("High"),
        "Medium": item.get("Medium"),
        "Low": item.get("Low"),
        "Info": item.get("Info"),
        "RiskScore": item.get("RiskScore"),
        "QuantityLevel": item.get("QuantityLevel"),
        "StatisticsUpdateDate": item.get("StatisticsUpdateDate"),
        "StatisticsUpToDate": item.get("StatisticsUpToDate"),
        "IsPublic": item.get("IsPublic"),
        "IsLocked": item.get("IsLocked"),
    }


def construct_result_data(item):
    return {
        "Id": item.get("Id"),
        "ResultId": item.get("ResultId"),
        "ScanId": item.get("ScanId"),
        "SimilarityId": item.get("SimilarityId"),
        "RawPriority": item.get("RawPriority"),
        "PathId": item.get("PathId"),
        "ConfidenceLevel": item.get("ConfidenceLevel"),
        "Date": item.get("Date"),
        "Severity": item.get("Severity"),
        "StateId": item.get("StateId"),
        "AssignedToUserId": item.get("AssignedToUserId"),
        "AssignedTo": item.get("AssignedTo"),
        "Comment": item.get("Comment"),
        "QueryId": item.get("QueryId"),
        "QueryVersionId": item.get("QueryVersionId"),
    }


def construct_query_data(item):
    return {
        "Id": item.get("Id"),
        "Name": item.get("Name"),
        "Version": item.get("Version"),
        "Severity": item.get("Severity"),
        "Comments": item.get("Comments"),
        "CxDescriptionId": item.get("CxDescriptionId"),
        "CweId": item.get("CweId"),
        "QuerySourceId": item.get("QuerySourceId"),
        "QueryGroupId": item.get("QueryGroupId"),
    }


def construct_result_state_data(item):
    return {
        "Id": item.get("Id"),
        "Name": item.get("Name"),
    }
