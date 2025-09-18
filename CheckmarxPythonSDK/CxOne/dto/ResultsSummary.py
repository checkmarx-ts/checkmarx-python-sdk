from dataclasses import dataclass
from .SastCounters import SastCounters, construct_sast_counters
from .KicsCounters import KicsCounters, construct_kics_counters
from .ScaCounters import ScaCounters, construct_sca_counters
from .ScaPackageCounters import ScaPackageCounters, construct_sca_package_counters
from .ScaContainersCounters import ScaContainersCounters, construct_sca_containers_counters
from .ApiSecCounters import ApiSecCounters, construct_api_sec_counters


@dataclass
class ResultsSummary:
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
    scan_id: str
    sast_counters: SastCounters
    kics_counters: KicsCounters
    sca_counters: ScaCounters
    sca_packages_counters: ScaPackageCounters
    sca_containers_counters: ScaContainersCounters
    api_sec_counters: ApiSecCounters


def construct_results_summary(item):
    return ResultsSummary(
        scan_id=item.get("scanId"),
        sast_counters=construct_sast_counters(item.get("sastCounters")),
        kics_counters=construct_kics_counters(item.get("kicsCounters")),
        sca_counters=construct_sca_counters(item.get("scaCounters")),
        sca_packages_counters=construct_sca_package_counters(item.get("scaPackagesCounters")),
        sca_containers_counters=construct_sca_containers_counters(item.get("scaContainersCounters")),
        api_sec_counters=construct_api_sec_counters(item.get("apiSecCounters"))
    )
