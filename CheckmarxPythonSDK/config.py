import os
import configparser
import pathlib

from optparse import OptionParser, SUPPRESS_HELP


def get_config_info_from_config_file():
    """

    Returns:
        dictionary
    """
    config_info = {}
    # the absolute path of the file config.ini
    config_file_path = pathlib.Path.home() / ".Checkmarx/config.ini"
    try:
        config_file = config_file_path.resolve(strict=True)
        parser_obj = configparser.ConfigParser(interpolation=configparser.BasicInterpolation())
        parser_obj.read(config_file)
        config_info = dict(parser_obj["checkmarx"])
    except FileNotFoundError:
        print("config.ini not found under ~/.Checkmarx/ directory.")

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

    return config_info


def get_config_info_from_command_line_arguments():
    """

    Returns:
        dictionary
    """
    config_info = {}
    parser = OptionParser()
    parser.add_option("--cxsast_base_url", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_username", help=SUPPRESS_HELP)
    parser.add_option("--cxsast_password", help=SUPPRESS_HELP)

    (options, args) = parser.parse_args()

    if options.cxsast_base_url:
        config_info.update({"base_url": options.cxsast_base_url})

    if options.cxsast_username:
        config_info.update({"username": options.cxsast_username})

    if options.cxsast_password:
        config_info.update({"password": options.cxsast_password})

    return config_info


def get_config_info():
    config_info = {}

    def get():
        nonlocal config_info
        if not config_info:
            # first, try to get config info from config.ini file in the ~/.Checkmarx folder
            config_info = get_config_info_from_config_file()

            # second, try to get config info from environment variables
            config_info.update(get_config_info_from_environment_variables())

            # third, try to get config info from command line arguments
            config_info.update(get_config_info_from_command_line_arguments())

            # if any one of the 3 variables are not set, we will raise an error
            if not config_info.get("base_url"):
                raise NameError("Checkmarx CxSAST Server base_url not set")
            if not config_info.get("username"):
                raise NameError("Checkmarx CxSAST Server username not set")
            if not config_info.get("password"):
                raise NameError("Checkmarx CxSAST Server password not set")
        return config_info

    return get()


max_try = 3
