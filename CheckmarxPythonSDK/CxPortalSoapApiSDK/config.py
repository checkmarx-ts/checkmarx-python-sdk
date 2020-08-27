# encoding: utf-8
import configparser
import pathlib

config_folder = pathlib.Path(__file__).parent.absolute()
config_file_path = pathlib.Path.home() / ".Checkmarx/config.ini"


def get_config(config_file=config_file_path):
    """

    Args:
        config_file: config.ini

    Returns:
        dict (base_url, username, password)
    """

    try:
        config_file = config_file.resolve()
    except FileNotFoundError:
        print("config.ini not found under config directory.")

    parser_obj = configparser.ConfigParser(interpolation=configparser.BasicInterpolation())
    parser_obj.read(config_file)
    cx_portal_config = parser_obj["checkmarx"]

    return {
        "base_url": cx_portal_config.get("base_url", "http://localhost:80"),
        "username": cx_portal_config.get("username", "Admin"),
        "password": cx_portal_config.get("password", "Password01!")
    }


config_data = get_config()
