from dataclasses import dataclass


@dataclass
class DastCliSettings:
    """Request-side cliSettings for POST /api/dast/scans/environment."""
    output: str = None
    retry: int = None
    retry_delay: int = None
    update_interval: int = None
    jvm_properties: str = None
    log_level: str = None

    def to_dict(self) -> dict:
        raw = {
            "output": self.output,
            "retry": self.retry,
            "retryDelay": self.retry_delay,
            "updateInterval": self.update_interval,
            "jvmProperties": self.jvm_properties,
            "logLevel": self.log_level,
        }
        return {k: v for k, v in raw.items() if v is not None}
