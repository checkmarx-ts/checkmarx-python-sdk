import logging
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from CheckmarxPythonSDK.utilities.configUtility import get_debug_command_line_arg

# create logger
logger = logging.getLogger("CheckmarxPythonSDK")
is_debug = get_debug_command_line_arg()
if is_debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
if is_debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

disable_warnings(InsecureRequestWarning)
