from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from CheckmarxPythonSDK.logger_setup import initialize_root_logger

# Initialize root logger
logger = initialize_root_logger()

disable_warnings(InsecureRequestWarning)
