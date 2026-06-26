from dataclasses import dataclass, asdict


@dataclass
class ScaRegistryConfigRequest:
    """Request body for creating a private registry configuration.

    Attributes:
        configurationName (str): A name for the configuration.
        content (str): The content of the configuration (XML for NuGet/Maven,
            INI-style for NPM).
        packageManager (str): The package manager of the repo associated with
            this configuration (e.g. 'nuget', 'maven', 'npm').
    """

    configurationName: str
    content: str
    packageManager: str

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
