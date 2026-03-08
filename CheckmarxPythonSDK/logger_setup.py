
import logging
from typing import Optional
from CheckmarxPythonSDK.utilities.configUtility import get_debug_command_line_arg

_ROOT_LOGGER_NAME = "CheckmarxPythonSDK"
_initialized = False
_root_logger = None


def _get_logging_level(level_str: Optional[str]) -> int:
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    if level_str and level_str.upper() in level_map:
        return level_map[level_str.upper()]
    return logging.INFO


def initialize_root_logger() -> logging.Logger:
    global _initialized, _root_logger
    
    if _initialized and _root_logger:
        return _root_logger
    
    logger = logging.getLogger(_ROOT_LOGGER_NAME)
    
    is_debug = get_debug_command_line_arg()
    if is_debug:
        base_level = logging.DEBUG
    else:
        base_level = logging.INFO
    
    if not logger.handlers:
        logger.setLevel(base_level)
        ch = logging.StreamHandler()
        ch.setLevel(base_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False
    
    _root_logger = logger
    _initialized = True
    return logger


def set_module_logger_level(module_name: str, logging_level: Optional[str]) -> None:
    logger_name = f"{_ROOT_LOGGER_NAME}.{module_name}"
    logger = logging.getLogger(logger_name)
    level = _get_logging_level(logging_level)
    logger.setLevel(level)
    
    for handler in logger.handlers:
        handler.setLevel(level)


def get_module_logger(module_name: str) -> logging.Logger:
    logger_name = f"{_ROOT_LOGGER_NAME}.{module_name}"
    return logging.getLogger(logger_name)
