
class DebugMessage(object):
    def __init__(self, message_line: int = None, debug_message: str = None, timestamp: str = None):
        self.messageLine = message_line
        self.debugMessage = debug_message
        self.timestamp = timestamp

    def __str__(self):
        return (f"DebugMessage(messageLine={self.messageLine}, "
                f"debugMessage={self.debugMessage}, timestamp={self.timestamp})")
