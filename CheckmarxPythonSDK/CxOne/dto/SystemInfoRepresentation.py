from dataclasses import dataclass


@dataclass
class SystemInfoRepresentation:
    file_encoding: ... = None
    java_home: ... = None
    java_runtime: ... = None
    java_vendor: ... = None
    java_version: ... = None
    java_vm: ... = None
    java_vm_version: ... = None
    os_architecture: ... = None
    os_name: ... = None
    os_version: ... = None
    server_time: ... = None
    uptime: ... = None
    uptime_millis: ... = None
    user_dir: ... = None
    user_locale: ... = None
    user_name: ... = None
    user_timezone: ... = None
    version: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "SystemInfoRepresentation":
        return cls(
            file_encoding=item.get("fileEncoding"),
            java_home=item.get("javaHome"),
            java_runtime=item.get("javaRuntime"),
            java_vendor=item.get("javaVendor"),
            java_version=item.get("javaVersion"),
            java_vm=item.get("javaVm"),
            java_vm_version=item.get("javaVmVersion"),
            os_architecture=item.get("osArchitecture"),
            os_name=item.get("osName"),
            os_version=item.get("osVersion"),
            server_time=item.get("serverTime"),
            uptime=item.get("uptime"),
            uptime_millis=item.get("uptimeMillis"),
            user_dir=item.get("userDir"),
            user_locale=item.get("userLocale"),
            user_name=item.get("userName"),
            user_timezone=item.get("userTimezone"),
            version=item.get("version"),
        )
