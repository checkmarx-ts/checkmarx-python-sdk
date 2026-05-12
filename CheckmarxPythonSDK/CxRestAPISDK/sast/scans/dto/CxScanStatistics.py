from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CxScanStatistics:

    id: Optional[int] = None
    scan_id: Optional[int] = None
    scan_status: Optional[str] = None
    product_version: Optional[str] = None
    engine_version: Optional[str] = None
    memory_peak_in_mb: Optional[int] = None
    virtual_memory_peak_in_mb: Optional[int] = None
    is_incremental_scan: Optional[bool] = None
    results_count: Optional[int] = None
    total_unscanned_files_count: Optional[int] = None
    file_count_of_detected_but_not_scanned_languages: Optional[List] = None
    total_filtered_parsed_loc: Optional[int] = None
    total_unfiltered_parsed_loc: Optional[int] = None
    language_statistics: Optional[List] = None
    path_filter_pattern: Optional[str] = None
    failed_queries_count: Optional[int] = None
    succeeded_general_queries_count: Optional[int] = None
    failed_general_queries_count: Optional[int] = None
    failed_stages: Optional[str] = None
    engine_operating_system: Optional[str] = None
    engine_pack_version: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanStatistics":
        return cls(
            id=item.get("id"),
            scan_id=item.get("scanId"),
            scan_status=item.get("scanStatus"),
            product_version=item.get("productVersion"),
            engine_version=item.get("engineVersion"),
            memory_peak_in_mb=item.get("memoryPeakInMB"),
            virtual_memory_peak_in_mb=item.get("virtualMemoryPeakInMB"),
            is_incremental_scan=item.get("isIncrementalScan"),
            results_count=item.get("resultsCount"),
            total_unscanned_files_count=item.get("totalUnScannedFilesCount"),
            file_count_of_detected_but_not_scanned_languages=list(
                item.get("fileCountOfDetectedButNotScannedLanguages", {}).items()
            ),
            total_filtered_parsed_loc=item.get("totalFilteredParsedLOC"),
            total_unfiltered_parsed_loc=item.get("totalUnFilteredParsedLOC"),
            language_statistics=item.get("languageStatistics"),
            path_filter_pattern=item.get("pathFilterPattern"),
            failed_queries_count=item.get("failedQueriesCount"),
            succeeded_general_queries_count=(item.get("generalQueries") or {}).get(
                "succeededGeneralQueriesCount"
            ),
            failed_general_queries_count=(item.get("generalQueries") or {}).get(
                "failedGeneralQueriesCount"
            ),
            failed_stages=item.get("failedStages"),
            engine_operating_system=item.get("engineOperatingSystem"),
            engine_pack_version=item.get("enginePackVersion"),
        )
