import time
from datetime import datetime
from os.path import normpath, join, dirname, exists

from CheckmarxPythonSDK.CxReporting.api import (
    get_report
)

from CheckmarxPythonSDK.CxReporting.dto import (
    CreateReportDTO,
    FilterDTO
)


def create_a_new_report_with_application_template_pdf():
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

    report_content = get_report(report_request=report_request)

    report_folder = dirname(__file__)
    time_stamp = datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
    file_name = normpath(join(report_folder, report_name + time_stamp + "." + output_format))
    with open(str(file_name), "wb") as f_out:
        f_out.write(report_content)


if __name__ == '__main__':
    create_a_new_report_with_application_template_pdf()
