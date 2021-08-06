class CxScanStatistics(object):

    def __init__(self, statistics_id, scan_id, scan_status, product_version, engine_version, memory_peak_in_mb,
                 virtual_memory_peak_in_mb, is_incremental_scan, results_count, total_unscanned_files_count,
                 file_count_of_detected_but_not_scanned_languages, total_filtered_parsed_loc,
                 total_unfiltered_parsed_loc, language_statistics, exclusion_folders_pattern, exclusion_files_pattern,
                 failed_queries_count, succeeded_general_queries_count, failed_general_queries_count,
                 failed_stages, engine_operating_system, engine_pack_version):
        """

        Args:
            statistics_id (int):
            scan_id (int):
            scan_status (str, optional):
            product_version (str):
            engine_version (str):
            memory_peak_in_mb (int):
            virtual_memory_peak_in_mb (int):
            is_incremental_scan (bool):
            results_count (int):
            total_unscanned_files_count (int):
            file_count_of_detected_but_not_scanned_languages (`list` of `CxScanFileCountOfLanguage`):
            total_filtered_parsed_loc (int):
            total_unfiltered_parsed_loc (int):
            language_statistics (`list` of `CxLanguageStatistic`):
            exclusion_folders_pattern (str):
            exclusion_files_pattern (str):
            failed_queries_count (int):
            succeeded_general_queries_count (int):
            failed_general_queries_count (int)
            failed_stages (str, optional):
            engine_operating_system (str):
            engine_pack_version (str):
        """
        self.id = statistics_id
        self.scan_id = scan_id
        self.scan_status = scan_status
        self.product_version = product_version
        self.engine_version = engine_version
        self.memory_peak_in_mb = memory_peak_in_mb
        self.virtual_memory_peak_in_mb = virtual_memory_peak_in_mb
        self.is_incremental_scan = is_incremental_scan
        self.results_count = results_count
        self.total_unscanned_files_count = total_unscanned_files_count
        self.file_count_of_detected_but_not_scanned_languages = file_count_of_detected_but_not_scanned_languages
        self.total_filtered_parsed_loc = total_filtered_parsed_loc
        self.total_unfiltered_parsed_loc = total_unfiltered_parsed_loc
        self.language_statistics = language_statistics
        self.exclusion_folders_pattern = exclusion_folders_pattern
        self.exclusion_files_pattern = exclusion_files_pattern
        self.failed_queries_count = failed_queries_count
        self.general_queries = {
            "succeededGeneralQueriesCount": succeeded_general_queries_count,
            "failedGeneralQueriesCount": failed_general_queries_count,
        }
        self.failed_stages = failed_stages
        self.engine_operating_system = engine_operating_system
        self.engine_pack_version = engine_pack_version

    def __str__(self):
        return """CxScanStatistics(statistics_id={}, scan_id={}, scan_status={}, product_version={}, engine_version={}, 
                memory_peak_in_mb={}, virtual_memory_peak_in_mb={}, is_incremental_scan={}, results_count={}, 
                total_unscanned_files_count={}, file_count_of_detected_but_not_scanned_languages={}, 
                total_filtered_parsed_loc={}, total_unfiltered_parsed_loc={}, language_statistics={}, 
                exclusion_folders_pattern={}, exclusion_files_pattern={}, failed_queries_count={}, general_queries={}, 
                failed_stages={}, engine_operating_system={}, 
                engine_pack_version={})""".format(self.id, self.scan_id, self.scan_status,
                                                  self.product_version, self.engine_version, self.memory_peak_in_mb,
                                                  self.virtual_memory_peak_in_mb, self.is_incremental_scan,
                                                  self.results_count, self.total_unscanned_files_count,
                                                  self.file_count_of_detected_but_not_scanned_languages,
                                                  self.total_filtered_parsed_loc,
                                                  self.total_unfiltered_parsed_loc, self.language_statistics,
                                                  self.exclusion_folders_pattern, self.exclusion_files_pattern,
                                                  self.failed_queries_count, self.general_queries, self.failed_stages,
                                                  self.engine_operating_system, self.engine_pack_version)
