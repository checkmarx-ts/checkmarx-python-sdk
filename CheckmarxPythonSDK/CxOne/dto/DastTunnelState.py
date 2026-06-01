from .StrEnum import StrEnum


class DastTunnelState(StrEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    NO_TUNNEL = "no_tunnel"
