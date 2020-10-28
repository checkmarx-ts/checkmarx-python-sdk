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


def get_config_info_from_config_file():
    """

    Returns:
        dictionary
    """
    config_info = {}

    home_directory = os.path.expanduser("~")
    # the absolute path of the file config.ini
    config_file_path = normpath(join(home_directory, ".Checkmarx/config.ini"))
    if not exists(config_file_path):
        print("config.ini not found under ~/.Checkmarx/ directory.")
    else:
        parser_obj = configparser.ConfigParser()
        parser_obj.read(config_file_path)
        config_info = {
            "base_url": parser_obj.get("checkmarx", "base_url"),
            "username": parser_obj.get("checkmarx", "username"),
            "password": parser_obj.get("checkmarx", "password"),
            "grant_type": "password",
            "scope": parser_obj.get("checkmarx", "scope"),
            "client_id": "resource_owner_client",
            "client_secret": "014DF517-39D1-4453-B7B3-9930C563627C"
        }

    return config_info


def get_config_info_from_environment_variables():
    """

    Returns:
        dictionary
    """
    config_info = {}

    if os.getenv("cxsast_base_url"):
        config_info.update({"base_url": os.getenv("cxsast_base_url")})

    if os.getenv("cxsast_username"):
        config_info.update({"username": os.getenv("cxsast_username")})

    if os.getenv("cxsast_password"):
        config_info.update({"password": os.getenv("cxsast_password")})

    if os.getenv("cxsast_grant_type"):
        config_info.update({"grant_type": os.getenv("cxsast_grant_type")})

    if os.getenv("cxsast_scope"):
        config_info.update({"scope": os.getenv("cxsast_scope")})

    if os.getenv("cxsast_client_id"):
        config_info.update({"client_id": os.getenv("cxsast_client_id")})

    if os.getenv("cxsast_client_secret"):
        config_info.update({"client_secret": os.getenv("cxsast_client_secret")})

    return config_info


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
    config_info = {}
    parser = PassThroughOptionParser()
    parser.add_option("--cxsast_base_url", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_username", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_password", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_grant_type", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_scope", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_client_id", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_client_secret", help=SUPPRESS_HELP)

    (options, args) = parser.parse_args()

    if options.cxsast_base_url:
        config_info.update({"base_url": options.cxsast_base_url})

    if options.cxsast_username:
        config_info.update({"username": options.cxsast_username})

    if options.cxsast_password:
        config_info.update({"password": options.cxsast_password})

    if options.cxsast_grant_type:
        config_info.update({"grant_type": options.cxsast_grant_type})

    if options.cxsast_scope:
        config_info.update({"scope": options.cxsast_scope})

    if options.cxsast_client_id:
        config_info.update({"client_id": options.cxsast_client_id})

    if options.cxsast_client_secret:
        config_info.update({"client_secret": options.cxsast_client_secret})

    return config_info


config = {
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
    "verify": False
}

# first, try to get config info from config.ini file in the ~/.Checkmarx folder
config.update(get_config_info_from_config_file())

# second, try to get config info from environment variables
config.update(get_config_info_from_environment_variables())

# third, try to get config info from command line arguments
config.update(get_config_info_from_command_line_arguments())
