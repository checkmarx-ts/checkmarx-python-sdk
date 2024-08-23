from .httpRequests import get_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import (
    ResultsSummary,
    KicsCounters,
    SastCounters,
    ScaCounters,
    ScaPackageCounters,
    ScaContainersCounters,
    ApiSecCounters,
)

api_url = "/api/scan-summary"


def get_summary_for_many_scans(scan_ids, include_severity_status=True, include_queries=False, include_files=False,
                               apply_predicates=True, language=None):
    """

    Args:
        scan_ids (list of str): Scan IDs to find. Each scan id will have his own object.
        include_severity_status (bool): if true returns the severityStatus field, otherwise will omit the field.
                            Default value : true
        include_queries (bool): if true returns the queries field, otherwise will omit the field.
                            Default value : false
        include_files (bool): if true returns the source code file and sink code file fields, otherwise will omit the fields.
                            Default value : false
        apply_predicates (bool): if true will apply changes from predicates, otherwise will return the raw results summary.
                            Default value : true
        language (str): get scan summary for specific source code language.

    Returns:
        dict
    """
    type_check(scan_ids, (list, tuple))
    type_check(include_severity_status, bool)
    type_check(include_queries, bool)
    type_check(include_files, bool)
    type_check(apply_predicates, bool)
    type_check(language, str)

    list_member_type_check(scan_ids, str)

    relative_url = api_url + "?"
    relative_url += get_url_param("scan-ids", scan_ids)
    relative_url += get_url_param("include-severity-status", include_severity_status)
    relative_url += get_url_param("include-queries", include_queries)
    relative_url += get_url_param("include-files", include_files)
    relative_url += get_url_param("apply-predicates", apply_predicates)
    relative_url += get_url_param("language", language)

    response = get_request(relative_url=relative_url)
    response = response.json()
    return {
        "scansSummaries": [
            ResultsSummary(
                scan_id=summary.get("scanId"),
                sast_counters=summary.get("sastCounters"),
                kics_counters=summary.get("kicsCounters"),
                sca_counters=summary.get("scaCounters"),
                sca_packages_counters=summary.get('scaPackagesCounters'),
                sca_containers_counters=summary.get('scaContainersCounters'),
                api_sec_counters=summary.get('apiSecCounters')
            ) for summary in response.get("scansSummaries") or []
        ],
        "totalCount": response.get("totalCount")
    }

