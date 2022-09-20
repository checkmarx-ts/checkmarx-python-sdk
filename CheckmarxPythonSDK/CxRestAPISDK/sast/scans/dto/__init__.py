from .scanSettings.CxCreateScanSettingsRequestBody import CxCreateScanSettingsRequestBody
from .scanSettings.CxCreateScanSettingsResponse import CxCreateScanSettingsResponse
from .scanSettings.CxEmailNotification import CxEmailNotification
from .scanSettings.CxLanguage import CxLanguage
from .scanSettings.CxScanSettings import CxScanSettings
from .CxCreateNewScanResponse import CxCreateNewScanResponse
from .CxDateAndTime import CxDateAndTime
from .CxFinishedScanStatus import CxFinishedScanStatus
from .CxLanguageState import CxLanguageState
from .CxPolicyFindingResponse import CxPolicyFindingResponse
from .CxPolicyFindingsStatus import CxPolicyFindingsStatus
from .CxRegisterScanReportResponse import CxRegisterScanReportResponse
from .CxResultsStatistics import CxResultsStatistics
from .CxScanQueueDetail import CxScanQueueDetail
from .CxScanReportStatus import CxScanReportStatus
from .CxScanReportXmlContent import CxScanReportXmlContent
from .CxScanResultAttackVector import CxScanResultAttackVector
from .CxScanResultAttackVectorByBFL import CxScanResultAttackVectorByBFL
from .CxScanResultLabelsFields import CxScanResultLabelsFields
from .CxScanResultNode import CxScanResultNode
from .CxScanStage import CxScanStage
from .CxScanState import CxScanState
from .CxScanType import CxScanType
from .CxSchedulingSettings import CxSchedulingSettings
from .CxStatisticsResult import CxStatisticsResult
from .CxStatus import CxStatus
from .CxStatusDetail import CxStatusDetail
from .CxLanguageStatistic import CxLanguageStatistic
from .CxScanFileCountOfLanguage import CxScanFileCountOfLanguage
from .CxScanStatistics import CxScanStatistics
from .CxScanParsedFiles import CxScanParsedFiles
from .CxScanParsedFilesMetric import CxScanParsedFilesMetric
from .CxScanFailedQueries import CxScanFailedQueries
from .CxScanFailedGeneralQueries import CxScanFailedGeneralQueries
from .CxScanSucceededGeneralQueries import CxScanSucceededGeneralQueries


def construct_scan_result_node(item):
    """

    Args:
        item (dict):

    Returns:

    """
    return CxScanResultNode(
        node_id=item.get("id"),
        order=item.get("order"),
        short_name=item.get('shortName'),
        full_name=item.get('fullName'),
        file_name=item.get('fileName'),
        folder=item.get('folder'),
        line=item.get('line'),
        column=item.get('column'),
        length=item.get('length'),
        method_line=item.get('methodLine'),
        source_url=item.get('sourceUrl'),
    )


def construct_attack_vector(ac):
    """

    Args:
        ac (dict): attack vector dictionary

    Returns:

    """
    return CxScanResultAttackVector(
        result_id=ac.get('resultId'),
        best_fix_location_node=ac.get('bestFixLocationNode'),
        nodes=[
            construct_scan_result_node(item) for item in ac.get("nodes")
        ]
    )
