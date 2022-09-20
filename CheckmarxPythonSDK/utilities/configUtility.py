import sys
import os
import json
from os.path import normpath, join, exists
from requests.compat import is_py2

if is_py2:
    import ConfigParser

    configparser = ConfigParser
else:
    import configparser

    configparser = configparser

from optparse import (OptionParser, SUPPRESS_HELP, BadOptionError, AmbiguousOptionError)


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


def get_config_path(file_extention=".ini"):
    """

    By default, the configuration file path is "~/.Checkmarx/config.ini".
    otherwise, check environment variable "checkmarx_config_path", if exists, override the previous one
    finally, check command line option "--checkmarx_config_path", if exists, override the previous one
    Args:
        file_extention (str)

    Returns:
        config_file_path (str)
    """
    if file_extention not in [".ini", ".json"]:
        raise ValueError("configuration file extention file can only be .ini or .json")

    home_directory = os.path.expanduser("~")
    # the absolute path of the file config.ini
    relative_file_path = ".Checkmarx/config" + file_extention
    config_file_path = normpath(join(home_directory, relative_file_path))

    # check environment variable "checkmarx_config_path", if exists, override the previous one
    config_path_from_env = os.getenv("checkmarx_config_path")
    if config_path_from_env is not None:
        config_file_path = config_path_from_env

    # check command line option "--checkmarx_config_path", if exists, override the previous one
    parser = PassThroughOptionParser(add_help_option=False)
    parser.add_option("--checkmarx_config_path", help=SUPPRESS_HELP)
    (options, args) = parser.parse_args()
    config_path_from_command_line = options.checkmarx_config_path
    if config_path_from_command_line:
        config_file_path = config_path_from_command_line

    return config_file_path


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


def get_config_info_from_config_ini_file(section, option_list):
    """
    Args:
        section (str):
        option_list (list of str):
    Returns:
        dictionary
    """

    def get_option(option):
        try:
            if option in ["max_try", "timeout"]:
                value = parser_obj.getint(section, option)
            elif option in ["verify"]:
                value = parser_obj.getboolean(section, option)
            else:
                value = parser_obj.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = None
        return value

    config_file_path = get_config_path()

    if not exists(config_file_path) or not config_file_path.endswith(".ini"):
        return {}

    parser_obj = configparser.ConfigParser()
    parser_obj.read(config_file_path)
    option_value_list = [get_option(option) for option in option_list]
    return dict(zip(option_list, option_value_list))


def get_config_info_from_config_json_file(section, option_list):

    config_file_path = get_config_path(file_extention=".json")

    if not exists(config_file_path) or not config_file_path.endswith(".json"):
        return {}

    with open(file=config_file_path, mode="r") as json_file:
        json_obj = json.load(fp=json_file)
    section_obj = json_obj.get(section)
    option_value_list = [section_obj.get(option) for option in option_list]

    return dict(zip(option_list, option_value_list))


def get_config_info_from_environment_variables(prefix, option_list):
    """

    Args:
        prefix (str):
        option_list (list of str):

    Returns:
        dict
    """
    def get_value(option):
        env_var = prefix + option
        if option in ["max_try", "timeout"]:
            value = os.getenv(env_var)
            if value:
                value = int(value)
        elif option in ["verify"]:
            value = os.getenv(env_var)
            if value and value.lower() == "true":
                value = True
            else:
                value = False
        else:
            value = os.getenv(env_var)
        return value
    option_value_list = [get_value(option=option) for option in option_list]
    return dict(zip(option_list, option_value_list))


def get_config_info_from_command_line_arguments(prefix, option_list):
    """
    Args:
        prefix (str):
        option_list (list of str):
    Returns:
        dictionary
    """
    def get_value(option):
        cli_var = prefix + option
        if option in ["max_try", "timeout"]:
            value = options.__getattribute__(cli_var)
            if value:
                value = int(value)
        elif option in ["verify"]:
            value = options.__getattribute__(cli_var)
            if value and value.lower() == "true":
                value = True
            else:
                value = False
        else:
            value = options.__getattribute__(cli_var)
        return value
    parser = PassThroughOptionParser(add_help_option=False)
    for item in option_list:
        parser.add_option("--" + prefix + item, help=SUPPRESS_HELP)
    (options, args) = parser.parse_args()
    option_value_list = [get_value(option=item) for item in option_list]
    return dict(zip(option_list, option_value_list))


def get_password_from_keyring(section, username):
    """

    Args:
        section (str):
        username (str):

    Returns:
        str
    """
    import keyring
    if sys.platform.startswith('win32'):
        from keyring.backends import Windows
        keyring.set_keyring(Windows.WinVaultKeyring())

    return keyring.get_password(section, username)


def get_config(config_default, section, prefix):
    """

    Args:
        config_default (dict):
        section (str):
        prefix (str):

    Returns:
        dict
    """
    option_list = [key for key in config_default.keys()]

    config_from_ini_file = get_config_info_from_config_ini_file(section=section, option_list=option_list)
    config_from_ini_file = clean_null_terms(config_from_ini_file)

    config_from_json_file = get_config_info_from_config_json_file(section=section, option_list=option_list)
    config_from_json_file = clean_null_terms(config_from_json_file)

    config_from_env = get_config_info_from_environment_variables(prefix=prefix, option_list=option_list)
    config_from_env = clean_null_terms(config_from_env)

    config_from_cli = get_config_info_from_command_line_arguments(prefix=prefix, option_list=option_list)
    config_from_cli = clean_null_terms(config_from_cli)

    config = {}
    config.update(config_default)
    config.update(config_from_ini_file)
    config.update(config_from_json_file)
    config.update(config_from_env)
    config.update(config_from_cli)

    if os.getenv("use_keyring"):
        config.update({"password": get_password_from_keyring(section=section, username=config.get("username"))})

    return config
