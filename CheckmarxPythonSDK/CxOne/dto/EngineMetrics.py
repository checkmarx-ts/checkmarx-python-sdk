
class EngineMetrics(object):

    def __init__(self, scan_id, memory_peak, virtual_memory_peak, total_scanned_files_count, total_scanned_loc,
                 dom_objects_per_language, successful_loc_per_language, failed_loc_per_language,
                 file_count_of_detected_but_not_scanned_languages, scanned_files_per_language):
        """

        Args:
            scan_id (str):
            memory_peak (int):
            virtual_memory_peak (int):
            total_scanned_files_count (int):
            total_scanned_loc (int):
            dom_objects_per_language:
            successful_loc_per_language:
            failed_loc_per_language:
            file_count_of_detected_but_not_scanned_languages:
            scanned_files_per_language:
        """
        self.scan_id = scan_id
        self.memory_peak = memory_peak
        self.virtual_memory_peak = virtual_memory_peak
        self.total_scanned_files_count = total_scanned_files_count
        self.total_scanned_loc = total_scanned_loc
        self.dom_objects_per_language = dom_objects_per_language
        self.successful_loc_per_language = successful_loc_per_language
        self.failed_loc_per_language = failed_loc_per_language
        self.file_count_of_detected_but_not_scanned_languages = file_count_of_detected_but_not_scanned_languages
        self.scanned_files_per_language = scanned_files_per_language

    def __str__(self):
        return f"""EngineMetrics(
        scan_id={self.scan_id},
        memory_peak={self.memory_peak},
        virtual_memory_peak={self.virtual_memory_peak},
        total_scanned_files_count={self.total_scanned_files_count},
        total_scanned_loc={self.total_scanned_loc},
        dom_objects_per_language={self.dom_objects_per_language},
        successful_loc_per_language={self.successful_loc_per_language},
        failed_loc_per_language={self.failed_loc_per_language},
        file_count_of_detected_but_not_scanned_languages={self.file_count_of_detected_but_not_scanned_languages},
        scanned_files_per_language={self.scanned_files_per_language},
        )"""
