class ResultsSummary(object):
    def __init__(self, scan_id, sast_counters, kics_counters, sca_counters, sca_packages_counters,
                 sca_containers_counters, api_sec_counters):
        """

        Args:
            scan_id (str): ID of the scan
            sast_counters (SastCounters):
            kics_counters (KicsCounters):
            sca_counters (ScaCounters):
            sca_packages_counters (ScaPackageCounters):
            sca_containers_counters (ScaContainersCounters):
            api_sec_counters (ApiSecCounters)
        """
        self.scanId = scan_id
        self.sastCounters = sast_counters
        self.kicsCounters = kics_counters
        self.scaCounters = sca_counters
        self.scaPackagesCounters = sca_packages_counters
        self.scaContainersCounters = sca_containers_counters
        self.apiSecCounters = api_sec_counters

    def __str__(self):
        return """ResultsSummary(scanId={}, sastCounters={}, kicsCounters={}, scaCounters={}, 
        scaPackagesCounters={}, scaContainersCounters={}, apiSecCounters={})""".format(
            self.scanId, self.sastCounters, self.kicsCounters, self.scaCounters, self.scaPackagesCounters,
            self.scaContainersCounters, self.apiSecCounters
        )
