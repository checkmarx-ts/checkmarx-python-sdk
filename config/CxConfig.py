# encoding: utf-8
"""
Configuration of Checkmarx
"""

import configparser
import pathlib

config_folder = pathlib.Path(__file__).parent.absolute()
config_file_path = config_folder / "config.ini"


class CxConfig(object):
    """
    get configuration information from config.ini
    """

    def __init__(self, config_file=config_file_path):
        try:
            config_file = config_file.resolve()
        except FileNotFoundError:
            print("config.ini not found under config directory.")

        parser_obj = configparser.ConfigParser()
        parser_obj.read(config_file)
        self.cx_config = parser_obj["checkmarx"]

    @property
    def base_url(self):
        return self.cx_config.get("base_url", "https://localhost:80")

    @property
    def username(self):
        return self.cx_config.get("username", "Admin")

    @property
    def password(self):
        return self.cx_config.get("password", "Password01!")

    @property
    def grant_type(self):
        return self.cx_config.get("grant_type", "password")

    @property
    def scope(self):
        return self.cx_config.get("scope", "sast_rest_api")

    @property
    def client_id(self):
        return self.cx_config.get("client_id", "resource_owner_client")

    @property
    def client_secret(self):
        return self.cx_config.get("client_secret", "014DF517-39D1-4453-B7B3-9930C563627C")

    @property
    def url(self):
        return self.cx_config.get("url", self.base_url + "/cxrestapi")

    @property
    def scan_preset(self):
        return self.cx_config.get("scan_preset", "Checkmarx Default")

    @property
    def configuration(self):
        return self.cx_config.get("configuration", "Default Configuration")

    @property
    def team(self):
        return self.cx_config.get("team", r"CxServer\SP\Company\Users")
