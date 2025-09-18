from dataclasses import dataclass


@dataclass
class EngineMetrics:
    """

    Args:
        scan_id (str):
        memory_peak (int):
        virtual_memory_peak (int):
        total_scanned_files_count (int):
        total_scanned_loc (int):
        dom_objects_per_language (int):
        successful_loc_per_language (int):
        failed_loc_per_language (int):
        file_count_of_detected_but_not_scanned_languages (int):
        scanned_files_per_language (int):
    """
    scan_id: str
    memory_peak: int
    virtual_memory_peak: int
    total_scanned_files_count: int
    total_scanned_loc: int
    dom_objects_per_language: int
    successful_loc_per_language: int
    failed_loc_per_language: int
    file_count_of_detected_but_not_scanned_languages: int
    scanned_files_per_language: int


def construct_engine_metrics(item):
    return EngineMetrics(
        scan_id=item.get("scanId"),
        memory_peak=item.get("memoryPeak"),
        virtual_memory_peak=item.get("virtualMemoryPeak"),
        total_scanned_files_count=item.get("totalScannedFilesCount"),
        total_scanned_loc=item.get("totalScannedLoc"),
        dom_objects_per_language=item.get("domObjectsPerLanguage"),
        successful_loc_per_language=item.get("successfulLocPerLanguage"),
        failed_loc_per_language=item.get("failedLocPerLanguage"),
        file_count_of_detected_but_not_scanned_languages=item.get("fileCountOfDetectedButNotScannedLanguages"),
        scanned_files_per_language=item.get("scannedFilesPerLanguage")
    )
