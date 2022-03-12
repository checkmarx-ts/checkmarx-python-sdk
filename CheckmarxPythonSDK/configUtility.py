import os
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


def get_config_info_from_config_file(section, option_list):
    """
    Args:
        section (str):
        option_list (list of str):
    Returns:
        dictionary
    """

    def get_option(option):
        try:
            if option in ["max_try"]:
                value = parser_obj.getint(section, option)
            elif option in ["verify"]:
                value = parser_obj.getboolean(section, option)
            else:
                value = parser_obj.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = None
        return value

    config_file_path = get_config_path()

    if not exists(config_file_path):
        print("config file path not found: {path} ".format(path=config_file_path))
        return {}

    parser_obj = configparser.ConfigParser()
    parser_obj.read(config_file_path)
    option_value_list = [get_option(option) for option in option_list]
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
        if option in ["max_try"]:
            value = os.getenv(env_var)
            if value:
                value = int(value)
        elif option in ["verify"]:
            value = os.getenv(env_var)
            if value and value.lower() == "true":
                value = True
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
        if option in ["max_try"]:
            value = options.__getattribute__(cli_var)
            if value:
                value = int(value)
        elif option in ["verify"]:
            value = options.__getattribute__(cli_var)
            if value and value.lower() == "true":
                value = True
        else:
            value = options.__getattribute__(cli_var)
    parser = PassThroughOptionParser()
    for option in option_list:
        parser.add_option("--" + prefix + option, help=SUPPRESS_HELP)
    (options, args) = parser.parse_args()
    option_value_list = [get_value(option=option) for option in option_list]
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

    config_from_file = get_config_info_from_config_file(section=section, option_list=option_list)
    config_from_file = clean_null_terms(config_from_file)

    config_from_env = get_config_info_from_environment_variables(prefix=prefix, option_list=option_list)
    config_from_env = clean_null_terms(config_from_env)

    config_from_cli = get_config_info_from_command_line_arguments(prefix=prefix, option_list=option_list)
    config_from_cli = clean_null_terms(config_from_cli)

    config = {}
    config.update(config_default)
    config.update(config_from_file)
    config.update(config_from_env)
    config.update(config_from_cli)
    return config
