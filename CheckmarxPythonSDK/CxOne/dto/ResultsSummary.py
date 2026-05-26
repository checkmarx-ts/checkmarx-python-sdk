from dataclasses import dataclass
from .SastCounters import SastCounters
from .KicsCounters import KicsCounters
from .ScaCounters import ScaCounters
from .ScaPackageCounters import ScaPackageCounters
from .ScaContainersCounters import ScaContainersCounters
from .ApiSecCounters import ApiSecCounters


@dataclass
class ResultsSummary:
    scan_id: str = None
    sast_counters: SastCounters = None
    kics_counters: KicsCounters = None
    sca_counters: ScaCounters = None
    sca_packages_counters: ScaPackageCounters = None
    sca_containers_counters: ScaContainersCounters = None
    api_sec_counters: ApiSecCounters = None

    @classmethod
    def from_dict(cls, item: dict) -> "ResultsSummary":
        return cls(
            scan_id=item.get("scanId"),
            sast_counters=SastCounters.from_dict(item["sastCounters"]) if item.get("sastCounters") else None,
            kics_counters=KicsCounters.from_dict(item["kicsCounters"]) if item.get("kicsCounters") else None,
            sca_counters=ScaCounters.from_dict(item["scaCounters"]) if item.get("scaCounters") else None,
            sca_packages_counters=ScaPackageCounters.from_dict(item["scaPackagesCounters"]) if item.get("scaPackagesCounters") else None,
            sca_containers_counters=ScaContainersCounters.from_dict(item["scaContainersCounters"]) if item.get("scaContainersCounters") else None,
            api_sec_counters=ApiSecCounters.from_dict(item["apiSecCounters"]) if item.get("apiSecCounters") else None,
        )
