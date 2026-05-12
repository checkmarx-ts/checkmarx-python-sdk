from dataclasses import dataclass


@dataclass
class EngineMetrics:
    scan_id: str = None
    memory_peak: int = None
    virtual_memory_peak: int = None
    total_scanned_files_count: int = None
    total_scanned_loc: int = None
    dom_objects_per_language: int = None
    successful_loc_per_language: int = None
    failed_loc_per_language: int = None
    file_count_of_detected_but_not_scanned_languages: int = None
    scanned_files_per_language: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "EngineMetrics":
        return cls(
            scan_id=item.get("scanId"),
            memory_peak=item.get("memoryPeak"),
            virtual_memory_peak=item.get("virtualMemoryPeak"),
            total_scanned_files_count=item.get("totalScannedFilesCount"),
            total_scanned_loc=item.get("totalScannedLoc"),
            dom_objects_per_language=item.get("domObjectsPerLanguage"),
            successful_loc_per_language=item.get("successfulLocPerLanguage"),
            failed_loc_per_language=item.get("failedLocPerLanguage"),
            file_count_of_detected_but_not_scanned_languages=item.get(
                "fileCountOfDetectedButNotScannedLanguages"
            ),
            scanned_files_per_language=item.get("scannedFilesPerLanguage"),
        )
