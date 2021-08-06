# encoding: utf-8


class CxOsaLibrary(object):
    """
    osa libraries
    """

    def __init__(self, library_id, name, version, release_date, high_unique_vulnerability_count,
                 medium_unique_vulnerability_count, low_unique_vulnerability_count, not_exploitable_vulnerability_count,
                 newest_version, newest_version_release_date, number_of_versions_since_last_update,
                 confidence_level, match_type, licenses, outdated, severity, risk_score, locations, code_usage_status,
                 code_reference_count, package_repository=None):

        """

        Args:
            library_id (str):
            name (str):
            version (str):
            release_date (str):
            high_unique_vulnerability_count (int):
            medium_unique_vulnerability_count (int):
            low_unique_vulnerability_count (int):
            not_exploitable_vulnerability_count (int):
            newest_version (str):
            newest_version_release_date (str):
            number_of_versions_since_last_update (int):
            confidence_level (int):
            match_type (:obj:`CxOsaMatchType`):
            licenses (:obj:`list` of :obj:`str`):
            outdated (boolean):
            severity (:obj:`CxOsaSeverity`):
            risk_score (float):
            locations (:obj:`list` of :obj:`CxOsaLocation`):
            code_usage_status (str):
            code_reference_count (int):
            package_repository (str):
        """
        self.id = library_id
        self.name = name
        self.version = version
        self.release_date = release_date
        self.high_unique_vulnerability_count = high_unique_vulnerability_count
        self.medium_unique_vulnerability_count = medium_unique_vulnerability_count
        self.low_unique_vulnerability_count = low_unique_vulnerability_count
        self.not_exploitable_vulnerability_count = not_exploitable_vulnerability_count
        self.newest_version = newest_version
        self.newest_version_release_date = newest_version_release_date
        self.number_of_versions_since_last_update = number_of_versions_since_last_update
        self.confidence_level = confidence_level
        self.match_type = match_type
        self.licenses = licenses
        self.outdated = outdated
        self.severity = severity
        self.risk_score = risk_score
        self.locations = locations
        self.code_usage_status = code_usage_status
        self.code_reference_count = code_reference_count
        self.package_repository = package_repository

    def __str__(self):
        return """CxOsaLibraries(id={}, name={}, version={}, release_date={}, high_unique_vulnerability_count={},
                 medium_unique_vulnerability_count={}, low_unique_vulnerability_count={}, 
                 not_exploitable_vulnerability_count={}, newest_version={}, newest_version_release_date={}, 
                 number_of_versions_since_last_update={}, confidence_level={}, match_type={}, licenses={}, 
                 outdated={}, severity={}, risk_score={}, locations={}, code_usage_status={},
                 code_reference_count={}, package_repository={})""".format(
            self.id, self.name, self.version, self.release_date, self.high_unique_vulnerability_count,
            self.medium_unique_vulnerability_count, self.low_unique_vulnerability_count,
            self.not_exploitable_vulnerability_count, self.newest_version, self.newest_version_release_date,
            self.number_of_versions_since_last_update, self.confidence_level, self.match_type, self.licenses,
            self.outdated, self.severity, self.risk_score, self.locations, self.code_usage_status,
            self.code_reference_count, self.package_repository
        )
