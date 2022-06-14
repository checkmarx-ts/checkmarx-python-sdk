import json
from .FilterDTO import FilterDTO


class CreateReportDTO(object):
    def __init__(self, template_id, output_format, entity_id, report_name=None, filters=()):
        """

        Args:
            template_id (int): maximum: 6 minimum: 1
                                Unique ID of a specific Template.
                                Possible Values:
                                    1 for Scan Template Vulnerability Type oriented;
                                    2 for Scan Template Result State oriented;
                                    3 for Project Template;
                                    4 for Single Team Template;
                                    5 for Multi Teams Template;
                                    6 for Application Template
                                    7 for Executive Template
            output_format (str): Format of the report to be generated. Is not case sensitive.
            entity_id (list of str):
                            Unique ID.
                            For the Scan template: Scan Id;
                            For the Project template: Project Id;
                            For the Single Team template: Team full name;
                            For the Multiple Teams template: list of Teams full name split by comma;
                            For the application template: list of project Id split by comma
                            For the executive template: list of teams full name split by comma
            report_name (str):  maxLength: 150 nullable: true
                            "Report Name",  Name of the report to be generated. The service generates automatically a
                            report Id that will be concatenated with the specified report name
            filters (list of FilterDTO): nullable: true,
                        Filters to be applied in the report creation.
        """
        if not isinstance(template_id, int):
            raise ValueError("parameter template_id type should be int")
        if not isinstance(output_format, str):
            raise ValueError("parameter output type should be str")
        if not isinstance(entity_id, (list, tuple)):
            raise ValueError("parameter entity_id type should be list or tuple")
        for entity in entity_id:
            if not isinstance(entity, str):
                raise ValueError("All entity id should be str")
        if not isinstance(report_name, str):
            raise ValueError("parameter report_name type should be str")
        if filters:
            if not isinstance(filters, (list, tuple)):
                raise ValueError("parameter filters type should be list or tuple")
            for a_filter in filters:
                if not isinstance(a_filter, FilterDTO):
                    raise ValueError("all filters should be FilterDTO")

        if not (1 <= template_id <= 7):
            raise ValueError("parameter template_id not in range, minimum value 1, maximum value 6")
        if output_format.upper() not in ["PDF", "JSON"]:
            raise ValueError("parameter output_format should be either pdf or json")

        self.templateId = template_id
        self.entityId = entity_id
        self.reportName = report_name
        self.filters = filters
        self.outputFormat = output_format.upper()

    def __str__(self):
        return """CreateReportDTO(templateId={}, entityId={}, reportName={}, filters={}, outputFormat={})""".format(
            self.templateId, self.entityId, self.reportName, self.filters, self.outputFormat
        )

    def get_post_data(self):
        return json.dumps(
            {
                "templateId": self.templateId,
                "entityId": self.entityId,
                "reportName": self.reportName,
                "filters": [
                    {
                        "type": item.type,
                        "excludedValues": item.excludedValues,
                        "includedValues": item.includedValues,
                        "pattern": item.pattern,
                    } for item in self.filters
                ],
                "outputFormat": self.outputFormat
            }
        )
