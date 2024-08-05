class PresetSummary(object):

    def __init__(self, preset_id=None, name=None, description=None, associated_projects=None, custom=None,
                 is_tenant_default=None, is_migrated=None):
        """

        Args:
            preset_id:
            name:
            description:
            associated_projects:
            custom:
            is_tenant_default:
            is_migrated:
        """
        self.preset_id = preset_id
        self.name = name
        self.description = description
        self.associated_projects = associated_projects
        self.custom = custom
        self.is_tenant_default = is_tenant_default
        self.is_migrated = is_migrated

    def __str__(self):
        return f"""PresetSummary(
        preset_id={self.preset_id},
        name={self.name},
        description={self.description},
        associated_projects={self.associated_projects},
        custom={self.custom},
        is_tenant_default={self.is_tenant_default},
        is_migrated={self.is_migrated},
        )"""
