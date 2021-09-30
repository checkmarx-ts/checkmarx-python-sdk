import os
from os.path import normpath, join, exists
from requests.compat import is_py2

if is_py2:
    import ConfigParser

    configparser = ConfigParser
else:
    import configparser

    configparser = configparser

from optparse import OptionParser, SUPPRESS_HELP, BadOptionError, AmbiguousOptionError


def get_config_path():
    """

    By default, the configuration file path is "~/.Checkmarx/config.ini".
    otherwise, check environment variable "checkmarx_config_path", if exists, override the previous one
    finally, check command line option "--checkmarx_config_path", if exists, override the previous one

    Returns:
        config_file_path (str)
    """

    home_directory = os.path.expanduser("~")
    # the absolute path of the file config.ini
    config_file_path = normpath(join(home_directory, ".Checkmarx/config.ini"))

    # check environment variable "checkmarx_config_path", if exists, override the previous one
    config_path_from_env = os.getenv("checkmarx_config_path")
    if config_path_from_env:
        config_file_path = config_path_from_env

    # check command line option "--checkmarx_config_path", if exists, override the previous one
    parser = PassThroughOptionParser()
    parser.add_option("--checkmarx_config_path", help=SUPPRESS_HELP)
    (options, args) = parser.parse_args()
    config_path_from_command_line = options.checkmarx_config_path
    if config_path_from_command_line:
        config_file_path = config_path_from_command_line

    return config_file_path


def get_config_info_from_config_file():
    """

    Returns:
        dictionary
    """
    config_file_path = get_config_path()

    if not exists(config_file_path):
        print("config file path not found: {path} ".format(path=config_file_path))
        return {}

    parser_obj = configparser.ConfigParser()
    parser_obj.read(config_file_path)

    cxsast_config = None
    if parser_obj.has_section("checkmarx"):
        cxsast_config = {
            "base_url": parser_obj.get("checkmarx",
                                       "base_url") if parser_obj.has_option("checkmarx", "base_url") else None,
            "username": parser_obj.get("checkmarx",
                                       "username") if parser_obj.has_option("checkmarx", "username") else None,
            "password": parser_obj.get("checkmarx",
                                       "password") if parser_obj.has_option("checkmarx", "password") else None,
            "grant_type": parser_obj.get("checkmarx",
                                         "grant_type") if parser_obj.has_option("checkmarx", "grant_type") else None,
            "scope": parser_obj.get("checkmarx",
                                    "scope") if parser_obj.has_option("checkmarx", "scope") else None,
            "client_id": parser_obj.get("checkmarx",
                                        "client_id") if parser_obj.has_option("checkmarx", "client_id") else None,
            "client_secret": parser_obj.get("checkmarx",
                                            "client_secret") if parser_obj.has_option("checkmarx",
                                                                                      "client_secret") else None,
            "scan_preset": parser_obj.get("checkmarx",
                                          "scan_preset") if parser_obj.has_option("checkmarx",
                                                                                  "scan_preset") else None,
            "configuration": parser_obj.get("checkmarx",
                                            "configuration") if parser_obj.has_option("checkmarx",
                                                                                      "configuration") else None,
            "team_full_name": parser_obj.get("checkmarx",
                                             "team_full_name") if parser_obj.has_option("checkmarx",
                                                                                        "team_full_name") else None,
            "max_try": parser_obj.getint("checkmarx",
                                         "max_try") if parser_obj.has_option("checkmarx",
                                                                             "max_try") else None,
            "report_folder": parser_obj.get("checkmarx",
                                            "report_folder") if parser_obj.has_option("checkmarx",
                                                                                      "report_folder") else None,
        }

    cxsca_config = None
    if parser_obj.has_section("CxSCA"):
        cxsca_config = {
            "access_control_url": parser_obj.get("CxSCA", "access_control_url"),
            "server": parser_obj.get("CxSCA", "server") if parser_obj.has_option("CxSCA", "server") else None,
            "account": parser_obj.get("CxSCA", "account") if parser_obj.has_option("CxSCA", "account") else None,
            "username": parser_obj.get("CxSCA", "username") if parser_obj.has_option("CxSCA", "username") else None,
            "password": parser_obj.get("CxSCA", "password") if parser_obj.has_option("CxSCA", "password") else None,
        }

    return {
        "CxSAST": cxsast_config,
        "CxSCA": cxsca_config,
    }


def get_config_info_from_environment_variables():
    """

    Returns:
        dictionary
    """

    max_try = os.getenv("cxsast_max_try")
    if max_try:
        max_try = int(max_try)

    verify = os.getenv("cxsast_verify")
    verify = bool(verify) and verify.lower() == 'true'

    cxsast_config = {
        "base_url": os.getenv("cxsast_base_url"),
        "username": os.getenv("cxsast_username"),
        "password": os.getenv("cxsast_password"),
        "grant_type": os.getenv("cxsast_grant_type"),
        "scope": os.getenv("cxsast_scope"),
        "client_id": os.getenv("cxsast_client_id"),
        "client_secret": os.getenv("cxsast_client_secret"),
        "scan_preset": os.getenv("cxsast_scan_preset"),
        "configuration": os.getenv("cxsast_configuration"),
        "team_full_name": os.getenv("cxsast_team_full_name"),
        "max_try": max_try,
        "verify": verify,
        "report_folder": os.getenv("cxsast_report_folder"),
    }

    cxsca_config = {
        "access_control_url": os.getenv("cxsca_access_control_url"),
        "server": os.getenv("cxsca_server"),
        "account": os.getenv("cxsca_account"),
        "username": os.getenv("cxsca_username"),
        "password": os.getenv("cxsca_password"),
    }

    return {
        "CxSAST": cxsast_config,
        "CxSCA": cxsca_config,
    }


class PassThroughOptionParser(OptionParser):
    """
    An unknown option pass-through implementation of OptionParser.

    When unknown arguments are encountered, bundle with largs and try again,
    until rargs is depleted.

    sys.exit(status) will still be called if a known argument is passed
    incorrectly (e.g. missing arguments or bad argument types, etc.)
    """

    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self, largs, rargs, values)
            except (BadOptionError, AmbiguousOptionError) as e:
                largs.append(e.opt_str)


def get_config_info_from_command_line_arguments():
    """

    Returns:
        dictionary
    """
    parser = PassThroughOptionParser()
    parser.add_option("--cxsast_base_url", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_username", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_password", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_grant_type", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_scope", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_client_id", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_client_secret", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_scan_preset", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_configuration", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_team_full_name", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_max_try", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_report_folder", help=SUPPRESS_HELP)

    parser.add_option("--cxsca_access_control_url", help=SUPPRESS_HELP)
    parser.add_option("--cxsca_server", help=SUPPRESS_HELP)
    parser.add_option("--cxsca_account", help=SUPPRESS_HELP)
    parser.add_option("--cxsca_username", help=SUPPRESS_HELP)
    parser.add_option("--cxsca_password", help=SUPPRESS_HELP)

    (options, args) = parser.parse_args()

    max_try = options.cxsast_max_try
    if max_try:
        max_try = int(max_try)

    cxsast_config = {
        "base_url": options.cxsast_base_url,
        "username": options.cxsast_username,
        "password": options.cxsast_password,
        "grant_type": options.cxsast_grant_type,
        "scope": options.cxsast_scope,
        "client_id": options.cxsast_client_id,
        "client_secret": options.cxsast_client_secret,
        "scan_preset": options.cxsast_scan_preset,
        "configuration": options.cxsast_configuration,
        "team_full_name": options.cxsast_team_full_name,
        "max_try": max_try,
        "report_folder": options.cxsast_report_folder,
    }

    cxsca_config = {
        "access_control_url": options.cxsca_access_control_url,
        "server": options.cxsca_server,
        "account": options.cxsca_account,
        "username": options.cxsca_username,
        "password": options.cxsca_password,
    }

    return {
        "CxSAST": cxsast_config,
        "CxSCA": cxsca_config,
    }


global_config = {
    "CxSAST": {
        "base_url": "http://localhost:80",
        "username": "Admin",
        "password": "Password",
        "grant_type": "password",
        "scope": "sast_rest_api",
        "client_id": "resource_owner_client",
        "client_secret": "014DF517-39D1-4453-B7B3-9930C563627C",
        "scan_preset": "Checkmarx Default",
        "configuration": "Default Configuration",
        "team_full_name": "/CxServer",
        "max_try": 3,
        "verify": False,
        "report_folder": None
    },
    "CxSCA": {
        "access_control_url": "https://platform.checkmarx.net",
        "server": "https://api-sca.checkmarx.net",
        "account": None,
        "username": None,
        "password": None,
    },
}


def clean_null_terms(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = clean_null_terms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean


def update_config(all_config, config_by_user):
    user_sast_config = config_by_user.get("CxSAST")
    if user_sast_config:
        all_config["CxSAST"].update(user_sast_config)

    user_sca_config = config_by_user.get("CxSCA")
    if user_sca_config:
        all_config["CxSCA"].update(user_sca_config)

    return all_config


def update_global_config(all_config):
    # first, try to get config info from config.ini file in the ~/.Checkmarx folder
    config_1 = get_config_info_from_config_file()
    config_1 = clean_null_terms(config_1)

    # second, try to get config info from environment variables
    config_2 = get_config_info_from_environment_variables()
    config_2 = clean_null_terms(config_2)

    # third, try to get config info from command line arguments
    config_3 = get_config_info_from_command_line_arguments()
    config_3 = clean_null_terms(config_3)

    all_config = update_config(all_config, config_1)
    all_config = update_config(all_config, config_2)
    all_config = update_config(all_config, config_3)
    return all_config


global_config = update_global_config(global_config)

config = global_config.get("CxSAST")
sca_config = global_config.get("CxSCA")
