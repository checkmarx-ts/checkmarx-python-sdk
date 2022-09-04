import time
from .httpRequests import (get_request, post_request)
from CheckmarxPythonSDK.utilities.compat import (OK, CREATED)

from .dto import (
    CreateReportDTO,
)


def retrieve_the_file_of_a_specific_report(report_id):
    """

    Args:
        report_id (int):

    Returns:
        file content (binary string)
    """
    report_content = None
    relative_url = "/api/reports/{id}".format(id=report_id)
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        report_content = response.content
    return report_content


def create_a_new_report_request(report_request):
    """

    Args:
        report_request (CreateReportDTO):

    Returns:
        report_id (int)
    """
    report_id = None

    if not isinstance(report_request, CreateReportDTO):
        return report_id

    relative_url = "/api/reports"
    data = report_request.get_post_data()
    response = post_request(relative_url=relative_url, data=data)
    if response.status_code == CREATED:
        item = response.json()
        report_id = item.get("reportId")
    return report_id


def retrieve_the_status_of_a_specific_report(report_id):
    """

    Args:
        report_id (int):

    Returns:
        report_status (str)
            NEW
            PROCESSING
            FINISHED
    """
    report_status = None
    relative_url = "/api/reports/{id}/status".format(id=report_id)
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        item = response.json()
        report_status = item.get("reportStatus")
    return report_status


def get_report(report_request):
    """

    Args:
        report_request (CreateReportDTO):

    Returns:
        file content (binary string)
    """
    report_id = create_a_new_report_request(report_request=report_request)
    if not report_id:
        return None

    report_status = retrieve_the_status_of_a_specific_report(report_id=report_id)
    while report_status.upper() != "FINISHED":
        if "FAIL" in report_status.upper():
            print("Report generation failed!")
            return None
        report_status = retrieve_the_status_of_a_specific_report(report_id=report_id)
        print("report status: {}".format(report_status))
        time.sleep(2)

    return retrieve_the_file_of_a_specific_report(report_id=report_id)