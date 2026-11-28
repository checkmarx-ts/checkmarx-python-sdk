import io
import logging

import pytest

from CheckmarxPythonSDK import logger_setup as ls


@pytest.fixture()
def sdk_root():
    """The SDK root logger as initialize_root_logger() configures it: level
    INFO with a console handler at INFO (pytest's own capture handler is
    left untouched)."""
    root = logging.getLogger(ls._ROOT_LOGGER_NAME)
    root.setLevel(logging.INFO)
    root.propagate = False
    handler = logging.StreamHandler(io.StringIO())
    handler.setLevel(logging.INFO)
    root.addHandler(handler)
    yield root, handler
    root.removeHandler(handler)
    root.setLevel(logging.NOTSET)
    root.propagate = True
    for name in ("CxOne", "CxRestAPISDK"):
        logging.getLogger(f"{ls._ROOT_LOGGER_NAME}.{name}").setLevel(
            logging.NOTSET
        )


def test_module_debug_lowers_root_handler_and_is_emitted(sdk_root):
    root, handler = sdk_root
    ls.set_module_logger_level("CxOne", "DEBUG")
    assert handler.level == logging.DEBUG

    module_logger = ls.get_module_logger("CxOne").getChild("repoManagerAPI")
    assert module_logger.getEffectiveLevel() == logging.DEBUG
    module_logger.debug("hello-debug")
    assert "hello-debug" in handler.stream.getvalue()

    # modules that did not request a more verbose level stay quiet
    sibling = ls.get_module_logger("CxRestAPISDK").getChild("someModule")
    sibling.debug("should-not-appear")
    assert "should-not-appear" not in handler.stream.getvalue()


def test_less_verbose_module_level_does_not_lower_root_handler(sdk_root):
    root, handler = sdk_root
    ls.set_module_logger_level("CxOne", "ERROR")
    assert handler.level == logging.INFO
    assert ls.get_module_logger("CxOne").level == logging.ERROR


def test_invalid_level_falls_back_to_info(sdk_root):
    ls.set_module_logger_level("CxOne", "LOUD")
    assert ls.get_module_logger("CxOne").level == logging.INFO
