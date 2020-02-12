# encoding: utf-8


class SAMLServiceProvider(object):

    def __init__(self, assertion_consumer_service_url, certificate_file_name, certificate_subject, issuer):
        """

        Args:
            assertion_consumer_service_url (str):
            certificate_file_name (str):
            certificate_subject (str):
            issuer (str):
        """
        self.assertion_consumer_service_url = assertion_consumer_service_url
        self.certificate_file_name = certificate_file_name
        self.certificate_subject = certificate_subject
        self.issuer = issuer

    def __str__(self):
        return """SAMLServiceProvider(assertion_consumer_service_url={}, certificate_file_name={}, 
        certificate_subject={}, issuer={})""".format(
            self.assertion_consumer_service_url, self.certificate_file_name, self.certificate_subject, self.issuer
        )
