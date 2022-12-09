import logging


def get_debug_command_line_arg():
    """
    True if there is --cx_debug in the command line option
    Returns:
        bool
    """
    result = False
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('--cx_debug', action="store_true", dest="cx_debug", help="enable debug mode")
    options, args = parser.parse_args()
    if options.cx_debug:
        result = True
    return result


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
