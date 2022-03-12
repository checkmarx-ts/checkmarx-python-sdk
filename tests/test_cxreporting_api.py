import time
from datetime import datetime
from os.path import normpath, join, dirname, exists

from CheckmarxPythonSDK.CxReporting.api import (
    retrieve_the_file_of_a_specific_report,
    retrieve_the_status_of_a_specific_report,
    create_a_new_report_request
)

from CheckmarxPythonSDK.CxReporting.dto import (
    CreateReportDTO,
    FilterDTO
)


def check_report_generation_status_and_write_to_file(report_id, report_name, report_type):
    report_status = "NEW"
    while report_status.upper() != "FINISHED":
        report_status = retrieve_the_status_of_a_specific_report(report_id=report_id)
        print("report status: {}".format(report_status))
        if report_status.upper() == "FAILED":
            print("Report generation failed!")
            return
        # time.sleep(2)

    report_content = retrieve_the_file_of_a_specific_report(report_id=report_id)
    report_folder = dirname(__file__)
    time_stamp = datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
    file_name = normpath(join(report_folder, report_name + time_stamp + "." + report_type))
    with open(str(file_name), "wb") as f_out:
        f_out.write(report_content)


def test_create_a_new_report_with_application_template_pdf():
    template_id = 6
    output_format = "PDF"
    entity_id = ["2", "3", "5"]
    report_name = "application_pdf"
    filters = [
        FilterDTO(
            filter_type=1,
            excluded_values=["Information", "Low"],
            included_values=None,
            pattern=None
        )
    ]
    report_request = CreateReportDTO(
        template_id=template_id,
        output_format=output_format,
        entity_id=entity_id,
        report_name=report_name,
        filters=filters
    )
    report_id = create_a_new_report_request(report_request=report_request)
    assert report_id is not None
    check_report_generation_status_and_write_to_file(
        report_id,
        report_name=report_name,
        report_type=output_format
    )


def test_create_a_new_report_with_application_template_json():
    template_id = 6
    output_format = "JSON"
    entity_id = ["2", "3", "5"]
    report_name = "application_json"
    filters = [
        FilterDTO(
            filter_type=1,
            excluded_values=["Information", "Low"],
            included_values=None,
            pattern=None
        )
    ]
    report_request = CreateReportDTO(
        template_id=template_id,
        output_format=output_format,
        entity_id=entity_id,
        report_name=report_name,
        filters=filters
    )
    report_id = create_a_new_report_request(report_request=report_request)
    assert report_id is not None
    check_report_generation_status_and_write_to_file(
        report_id,
        report_name=report_name,
        report_type=output_format
    )
