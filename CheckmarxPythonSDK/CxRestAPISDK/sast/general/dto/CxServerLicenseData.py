# encoding: utf-8
import datetime
import logging
logger = logging.getLogger("CheckmarxPythonSDK")


class CxServerLicenseData(object):
    """
    CxSAST server license data
    """

    def __init__(self, current_audit_users, current_projects_count,
                 current_users, edition, expiration_date, hid, is_osa_enabled,
                 max_audit_users, max_concurrent_scans, max_loc, max_users,
                 osa_expiration_date, projects_allowed, supported_languages):
        self.current_audit_users = current_audit_users
        self.current_projects_count = current_projects_count
        self.current_users = current_users
        self.edition = edition
        self.expiration_date = parse_expiration_date(expiration_date)
        self.hid = hid
        self.is_osa_enabled = is_osa_enabled
        self.max_audit_users = max_audit_users
        self.max_concurrent_scans = max_concurrent_scans
        self.max_loc = max_loc
        self.max_users = max_users
        # If there is no OSA expiration date, an empty string is returned.
        # We coerce it to None
        if not osa_expiration_date:
            self.osa_expiration_date = None
        else:
            self.osa_expiration_date = parse_expiration_date(osa_expiration_date)
        self.projects_allowed = projects_allowed
        self.supported_languages = supported_languages

    def __str__(self):
        return """CxServerLicenseData(current_audit_users={},
               current_projects_count={}, current_users={}, edition={},
               expiration_date={}, hid={}, is_osa_enabled={},
               max_audit_users={}, max_concurrent_scans={}, max_loc={}
               max_users={}, osa_expiration_date={},
               projects_allowed={}, supported_languages={})""".format(
            self.current_audit_users, self.current_projects_count,
            self.current_users, self.edition, self.expiration_date,
            self.hid, self.is_osa_enabled, self.max_audit_users,
            self.max_concurrent_scans, self.max_loc, self.max_users,
            self.osa_expiration_date, self.projects_allowed,
            self.supported_languages
        )


def parse_expiration_date(date_str):
    """
    Parse a date string in MM/DD/YYYY format into a datetime.date object. If
    the string cannot be parsed, we return it instead.
    """
    bits = date_str.split('/')
    try:
        return datetime.date(int(bits[2]), int(bits[0]), int(bits[1]))
    except:
        logger.debug("Cannot parse {} as MM/DD/YYYY".format(date_str))
        return date_str
