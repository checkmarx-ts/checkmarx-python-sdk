# encoding: utf-8


class CxOsaLicense(object):
    """
    the license of a third party library
    """

    def __init__(self, license_id, name, risk_level, copyright_risk_score, patent_risk_score, copy_left, linking,
                 royality_free, reference_type, reference, url):
        """

        Args:
            license_id (str):
            name (str):
            risk_level (str): eg. "Low"
            copyright_risk_score (int):
            patent_risk_score (int):
            copy_left (str): eg. "No"
            linking (str): "Non_Viral"
            royality_free (str): "No"
            reference_type (str):
            reference (str, optional):
            url (str):
        """
        self.id = license_id
        self.name = name
        self.risk_level = risk_level
        self.copyright_risk_score = copyright_risk_score
        self.patent_risk_score = patent_risk_score
        self.copy_left = copy_left
        self.linking = linking
        self.royality_free = royality_free
        self.reference_type = reference_type
        self.reference = reference
        self.url = url

    def __str__(self):
        return """CxOsaLicenses(id={}, name={}, risk_level={}, copyright_risk_score={}, patent_risk_score={}, 
                copy_left={}, linking={}, royality_free={}, reference_type={}, reference={}, url={})""".format(
            self.id, self.name, self.risk_level, self.copyright_risk_score, self.patent_risk_score,
            self.copy_left, self.linking, self.royality_free, self.reference_type, self.reference, self.url
        )
