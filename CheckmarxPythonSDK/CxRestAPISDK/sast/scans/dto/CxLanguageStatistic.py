class CxLanguageStatistic(object):

    def __init__(self, language, parsed_successfully_count, parsed_unsuccessfully_count, parsed_partially_count,
                 successful_loc, unsuccessful_loc, scanned_successfully_loc_percentage, count_of_dom_objects):
        """

        Args:
            language (str):
            parsed_successfully_count (int):
            parsed_unsuccessfully_count (int):
            parsed_partially_count (int):
            successful_loc (int):
            unsuccessful_loc (int):
            scanned_successfully_loc_percentage (int):
            count_of_dom_objects (int):
        """
        self.language = language
        self.parsed_files = {
            "parsedSuccessfullyCount": parsed_successfully_count,
            "parsedUnsuccessfullyCount": parsed_unsuccessfully_count,
            "parsedPartiallyCount": parsed_partially_count,
        }

        self.scanned_loc_per_language = {
            "successfulLOC": successful_loc,
            "unsuccessfulLOC": unsuccessful_loc,
            "scannedSuccessfullyLOCPercentage": scanned_successfully_loc_percentage,
        }

        self.count_of_dom_object = count_of_dom_objects

    def __str__(self):
        return """CxLanguageStatistic(language={}, parsed_files={}, scanned_loc_per_language={}, 
                count_of_dom_object={})""".format(
            self.language, self.parsed_files, self.scanned_loc_per_language, self.count_of_dom_object
        )
