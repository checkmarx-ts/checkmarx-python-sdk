# encoding: utf-8

import xml.etree.ElementTree as eT


class CxScanReportXmlContent(object):
    """
    scan report xml content
    """

    def __init__(self, report_file_path):
        self.tree = eT.parse(report_file_path)
        self.root = self.tree.getroot()

    def filter_by_severity(self, high=False, medium=False, low=False, info=False):
        """
        filter at Query level

        Args:
            high (boolean):  True means keep, False means remove
            medium (boolean): True means keep, False means remove
            low (boolean): True means keep, False means remove
            info (boolean): True means keep, False means remove
        """
        for query in self.root.findall("Query"):
            severity = query.attrib.get("Severity")
            if ((severity == "High") and (not high)) \
                    or ((severity == "Medium") and (not medium)) \
                    or ((severity == "Low") and (not low)) \
                    or ((severity == "Information") and (not info)):
                self.root.remove(query)

    def filter_by_state(self, to_verify=False, not_exploitable=False, confirmed=False, urgent=False,
                        proposed_not_exploitable=False):
        """
        filter at Path level

        Args:
            to_verify (boolean): True means keep, False means remove
            not_exploitable (boolean): True means keep, False means remove
            confirmed (boolean): True means keep, False means remove
            urgent (boolean): True means keep, False means remove
            proposed_not_exploitable (boolean): True means keep, False means remove

        """
        states_list = [
            to_verify,
            not_exploitable,
            confirmed,
            urgent,
            proposed_not_exploitable
        ]
        for query in self.root.findall("Query"):
            for result in query.findall("Result"):
                state_index = result.attrib.get("state")
                if state_index and (not states_list[int(state_index)]):
                    query.remove(result)
            # remove the parent Result tag if it has no child element
            if query.find("Result") is None:
                self.root.remove(query)

    def filter_by_assign_to_user(self, user_list=None):
        """

        Args:
            user_list (:obj:`list` of :obj:`str`):
        """
        if user_list:
            for query in self.root.findall("Query"):
                for result in query.findall("Result"):
                    assign_to_user = result.attrib.get("AssignToUser")
                    if assign_to_user:
                        for user in user_list:
                            if user not in assign_to_user:
                                query.remove(result)
                    else:
                        query.remove(result)
                # remove the parent Result tag if it has no child element
                if query.find("Result") is None:
                    self.root.remove(query)

    def filter_by_categories(self, categories_list=None):
        """

        Args:
            categories_list (:obj:`list` of :obj:`str`):
                example:
                [
                    PCI DSS v3.2,
                    OWASP Top 10 2013,
                    FISMA 2014,
                    NIST SP 800-53,
                    OWASP Top 10 2017
                ]
        """
        if categories_list:
            for query in self.root.findall("Query"):
                categories = query.attrib.get("categories")
                if categories:
                    ca = [item.split(";")[0] for item in categories.split(",")]
                    if not set(ca).intersection(set(categories_list)):
                        self.root.remove(query)
                else:
                    self.root.remove(query)

    def filter_by_query_names(self, query_names=None):
        """

        Args:
            query_names (:obj:`list` of :obj:`str`):
                example:
                [
                    Code_Injection,
                    Connection_String_Injection,
                    Reflected_XSS_All_Clients
                ]
        """
        if query_names:
            for query in self.root.findall("Query"):
                name = query.attrib.get("name")
                if name and (name not in query_names):
                    self.root.remove(query)

    def write_new_xml(self, new_xml_file_path):
        """
        write modified data into a new xml file

        Args:
            new_xml_file_path (str):
        """
        self.tree.write(new_xml_file_path)
