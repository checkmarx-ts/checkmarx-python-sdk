class SystemInfoRepresentation:
    def __init__(self, file_encoding, java_home, java_runtime, java_vendor, java_version, java_vm, java_vm_version,
                 os_architecture, os_name, os_version, server_time, uptime, uptime_millis, user_dir, user_locale,
                 user_name, user_timezone, version):
        self.fileEncoding = file_encoding
        self.javaHome = java_home
        self.javaRuntime = java_runtime
        self.javaVendor = java_vendor
        self.javaVersion = java_version
        self.javaVm = java_vm
        self.javaVmVersion = java_vm_version
        self.osArchitecture = os_architecture
        self.osName = os_name
        self.osVersion = os_version
        self.serverTime = server_time
        self.uptime = uptime
        self.uptimeMillis = uptime_millis
        self.userDir = user_dir
        self.userLocale = user_locale
        self.userName = user_name
        self.userTimezone = user_timezone
        self.version = version

    def __str__(self):
        return f"SystemInfoRepresentation(" \
               f"fileEncoding={self.fileEncoding} " \
               f"javaHome={self.javaHome} " \
               f"javaRuntime={self.javaRuntime} " \
               f"javaVendor={self.javaVendor} " \
               f"javaVersion={self.javaVersion} " \
               f"javaVm={self.javaVm} " \
               f"javaVmVersion={self.javaVmVersion} " \
               f"osArchitecture={self.osArchitecture} " \
               f"osName={self.osName} " \
               f"osVersion={self.osVersion} " \
               f"serverTime={self.serverTime} " \
               f"uptime={self.uptime} " \
               f"uptimeMillis={self.uptimeMillis} " \
               f"userDir={self.userDir} " \
               f"userLocale={self.userLocale} " \
               f"userName={self.userName} " \
               f"userTimezone={self.userTimezone} " \
               f"version={self.version} " \
               f")"

    def to_dict(self):
        return {
            "fileEncoding": self.fileEncoding,
            "javaHome": self.javaHome,
            "javaRuntime": self.javaRuntime,
            "javaVendor": self.javaVendor,
            "javaVersion": self.javaVersion,
            "javaVm": self.javaVm,
            "javaVmVersion": self.javaVmVersion,
            "osArchitecture": self.osArchitecture,
            "osName": self.osName,
            "osVersion": self.osVersion,
            "serverTime": self.serverTime,
            "uptime": self.uptime,
            "uptimeMillis": self.uptimeMillis,
            "userDir": self.userDir,
            "userLocale": self.userLocale,
            "userName": self.userName,
            "userTimezone": self.userTimezone,
            "version": self.version,
        }


def construct_system_info_representation(item):
    return SystemInfoRepresentation(
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
