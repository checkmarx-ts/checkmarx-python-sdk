# encoding: utf-8

import xml.etree.ElementTree as eT


class CxScanReportXmlContent(object):
    """
    scan report xml content
    """

    def __init__(self, report_file_path):
        self.tree = eT.parse(report_file_path)
        self.root = self.tree.getroot()

    def filter_to_keep_xml_result_by_severity(self, high=True, medium=True, low=True, info=True):
        """
        filter at Query level
        :param high: boolean
            True means keep, False means remove
        :param medium: boolean
            True means keep, False means remove
        :param low: boolean
            True means keep, False means remove
        :param info: boolean
            True means keep, False means remove
        :return:
        """
        for query in self.root.findall("Query"):
            severity = query.attrib.get("Severity")
            if ((severity == "High") and (not high)) \
                    or ((severity == "Medium") and (not medium)) \
                    or ((severity == "Low") and (not low)) \
                    or ((severity == "Information") and (not info)):
                self.root.remove(query)

    def filter_to_keep_xml_result_by_state(self, to_verify=True, not_exploitable=True, confirmed=True, urgent=True,
                                           proposed_not_exploitable=True):
        """
        filter at Path level
        :param to_verify: boolean
            True means keep, False means remove
        :param not_exploitable：boolean
            True means keep, False means remove
        :param confirmed: boolean
            True means keep, False means remove
        :param urgent: boolean
            True means keep, False means remove
        :param proposed_not_exploitable: boolean
            True means keep, False means remove
        :return:
        """
        a_dict = {
            0: to_verify,
            1: not_exploitable,
            2: confirmed,
            3: urgent,
            4: proposed_not_exploitable
        }
        for query in self.root.findall("Query"):
            for result in query.findall("Result"):
                state = result.attrib.get("state")
                if state and (not a_dict.get(int(state))):
                    query.remove(result)
            # remove the parent Result tag if it has no child element
            if query.find("Result") is None:
                self.root.remove(query)

    def filter_to_keep_xml_result_by_assign_to_user(self, user_list=None):
        """

        :param user_list: list of str
        :return:
        """
        if user_list:
            for query in self.root.findall("Query"):
                for result in query.findall("Result"):
                    assign_to_user = result.attrib.get("AssignToUser")
                    if assign_to_user:
                        user_not_in_assigned_user = True
                        for user in user_list:
                            if user in assign_to_user:
                                user_not_in_assigned_user = False
                                break
                        if user_not_in_assigned_user:
                            query.remove(result)
                    else:
                        query.remove(result)
                # remove the parent Result tag if it has no child element
                if query.find("Result") is None:
                    self.root.remove(query)

    def filter_to_keep_xml_result_by_categories(self, categories_list=None):
        """

        :param categories_list: list of str
            example:
            [
                PCI DSS v3.2,
                OWASP Top 10 2013,
                FISMA 2014,
                NIST SP 800-53,
                OWASP Top 10 2017
            ]
        :return:
        """
        if categories_list:
            for query in self.root.findall("Query"):
                categories = query.attrib.get("categories")
                if categories:
                    ca = [item.split(";")[0] for item in categories.split(",")]
                    if len(set(ca).intersection(set(categories_list))) == 0:
                        self.root.remove(query)
                else:
                    self.root.remove(query)

    def filter_to_keep_xml_result_by_query_names(self, query_names=None):
        """

        :param query_names: list of query names
            example:
            [
                Code_Injection,
                Connection_String_Injection,
                Reflected_XSS_All_Clients
            ]
        :return:
        """
        if query_names:
            for query in self.root.findall("Query"):
                name = query.attrib.get("name")
                if name and (name not in query_names):
                    self.root.remove(query)

    def write_new_xml(self, new_xml_file_path):
        """
        write modified data into a new xml file
        :param new_xml_file_path: str
        :return:
        """
        self.tree.write(new_xml_file_path)
