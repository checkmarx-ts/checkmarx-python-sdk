from .StrEnum import StrEnum


class ResourceType(StrEnum):
    APPLICATION = "application"
    PROJECT = "project"
    TENANT = "tenant"
    TENANTGROUP = "tenantgroup"
    GLOBAL = "global"
