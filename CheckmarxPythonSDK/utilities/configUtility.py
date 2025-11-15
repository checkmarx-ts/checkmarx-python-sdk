import sys
import os
import json
import logging
from os.path import normpath, join, exists
logger = logging.getLogger("CheckmarxPythonSDK")

import configparser

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


def get_config_path(file_extension=".ini"):
    """

    By default, the configuration file path is "~/.Checkmarx/config.ini".
    otherwise, check environment variable "checkmarx_config_path", if exists, override the previous one
    finally, check command line option "--checkmarx_config_path", if exists, override the previous one
    Args:
        file_extension (str)

    Returns:
        config_file_path (str)
    """
    if file_extension not in [".ini", ".json"]:
        raise ValueError("configuration file extention file can only be .ini or .json")

    home_directory = os.path.expanduser("~")
    # the absolute path of the file config.ini
    relative_file_path = ".Checkmarx/config" + file_extension
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

    config_file_path = get_config_path(file_extension=".json")

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
            value = os.getenv(env_var) or os.getenv(env_var.upper())
            if value:
                value = int(value)
        if option in ["verify"]:
            value = os.getenv(env_var) or os.getenv(env_var.upper())
            if value and value.lower() == "false":
                value = False
            elif value and value.lower() == "true":
                value = True
            else:
                pass
        else:
            value = os.getenv(env_var) or os.getenv(env_var.upper())
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
        if option in ["verify"]:
            value = options.__getattribute__(cli_var)
            if value and value.lower() == "false":
                value = False
            elif value and value.lower() == "true":
                value = True
            else:
                pass
        else:
            value = options.__getattribute__(cli_var)
        return value
    parser = PassThroughOptionParser(add_help_option=False)
    for item in option_list:
        parser.add_option("--" + prefix + item, help=SUPPRESS_HELP)
    (options, args) = parser.parse_args()
    option_value_list = [get_value(option=item) for item in option_list]
    return dict(zip(option_list, option_value_list))


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
    logger.debug("default config value: {}".format(config_default))
    config.update(config_default)
    logger.debug("config from config.ini file: {}".format(config_from_ini_file))
    config.update(config_from_ini_file)
    logger.debug("override the config value, now the config value is: {}".format(config))
    logger.debug("config from config.json. file: {}".format(config_from_json_file))
    config.update(config_from_json_file)
    logger.debug("override the config value, now the config value is: {}".format(config))
    logger.debug("config_from_env: {}".format(config_from_env))
    config.update(config_from_env)
    logger.debug("override the config value, now the config value is: {}".format(config))
    logger.debug("config_from_cli: {}".format(config_from_cli))
    config.update(config_from_cli)
    logger.debug("override the config value, now the config value is: {}".format(config))
    config = clean_null_terms(config)
    logger.debug("final config value is: {}".format(config))
    return config


def get_debug_command_line_arg():
    """
    True if there is --cx_debug in the command line option
    Returns:
        bool
    """
    result = False
    import sys
    logger.debug(sys.argv)
    parser = PassThroughOptionParser(add_help_option=False)
    parser.add_option('--cx_debug', action="store_true", dest="cx_debug", help="enable debug mode")
    options, args = parser.parse_args()
    if options.cx_debug:
        result = True
    return result
