import warnings
from CheckmarxPythonSDK.logger_setup import initialize_root_logger

# Initialize root logger
logger = initialize_root_logger()

warnings.filterwarnings("ignore", message=".*SSL.*")
