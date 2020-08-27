# encoding: utf-8
from .config import get_config
from .auth import get_new_token
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)
